# roadmap/serializers.py (assuming your app is named 'roadmap')

from rest_framework import serializers
from .models import Roadmap, Topic, Subtopic, ChatMessage
from rest_framework.pagination import PageNumberPagination


class SubtopicSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subtopic model.
    Handles serialization and deserialization of individual subtopics.
    """
    class Meta:
        model = Subtopic
        fields = ['id', 'title'] # Only expose the title for subtopics


class TopicSerializer(serializers.ModelSerializer):
    """
    Serializer for the Topic model.
    Includes nested SubtopicSerializer to handle subtopics within a topic.
    """
    # Use the SubtopicSerializer to represent the 'subtopics' related_name
    # many=True indicates that there can be multiple subtopics
    # read_only=False (default) allows for deserialization (creation/update)
    subtopics = SubtopicSerializer(many=True)

    class Meta:
        model = Topic
        fields = ['title', 'importance_score', 'subtopics']


class RoadmapSerializer(serializers.ModelSerializer):
    """
    Serializer for the Roadmap model.
    Includes nested TopicSerializer to handle topics and their subtopics.
    This serializer will also handle the creation of nested objects.
    """
    # Use the TopicSerializer to represent the 'topics' related_name
    topics = TopicSerializer(many=True)

    class Meta:
        model = Roadmap
        fields = ['id', 'interviewer', 'topic', 'created_at', 'topics']
        # 'read_only_fields' can be used for fields that should not be set by the client
        read_only_fields = ['created_at'] # created_at is auto_now_add, so it's read-only


    def create(self, validated_data):
        """
        Custom create method to handle nested creation of Topic and Subtopic instances.
        When a POST request comes in for a Roadmap, this method extracts the nested
        'topics' data and creates them along with the Roadmap instance.
        """
        # Extract the nested 'topics' data from validated_data
        topics_data = validated_data.pop('topics')

        # Create the Roadmap instance first
        roadmap = Roadmap.objects.create(**validated_data)

        # Iterate over the extracted topics data
        for topic_data in topics_data:
            # Extract the nested 'subtopics' data for the current topic
            subtopics_data = topic_data.pop('subtopics')

            # Create the Topic instance, linking it to the newly created roadmap
            topic = Topic.objects.create(roadmap=roadmap, **topic_data)

            # Iterate over the extracted subtopics data
            for subtopic_data in subtopics_data:
                # Create the Subtopic instance, linking it to the newly created topic
                Subtopic.objects.create(topic=topic, **subtopic_data)

        return roadmap

    # You would typically also override update() if you need to handle nested updates
    # def update(self, instance, validated_data):
    #     # Logic for updating nested objects can be more complex
    #     # as you need to handle existing, new, and deleted nested items.
    #     # For simplicity, often nested updates are handled by deleting and recreating
    #     # or by custom logic to identify changes.
    #     pass

class RoadmapListSerializer(serializers.ModelSerializer):
    """
    A lightweight serializer for listing Roadmap instances,
    returning only a subset of fields.
    """
    class Meta:
        model = Roadmap
        fields = ['id', 'topic', 'interviewer', 'created_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatMessage model.
    Converts ChatMessage instances to JSON and vice-versa.
    """
    class Meta:
        model = ChatMessage
        # Fields to include in the serialized output.
        # 'subtopic' will be the ID of the related subtopic.
        fields = [
            'id',
            'subtopic',
            'user_message',
            'llm_response',
            'timestamp',
        ]
        # Make llm_response read-only for incoming data if it's always generated by LLM
        read_only_fields = ['timestamp']



class LatestTenMessagesPagination(PageNumberPagination):
    page_size = 10
    ordering = '-timestamp'  # latest first
