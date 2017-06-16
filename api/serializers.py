from rest_framework import serializers
from .models import User, Team
from rest_framework.reverse import reverse

import hashlib, random, string

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    verification_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'team', 'password', 'verification_url']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User(**validated_data)
        instance.verification_key = generate_verification_key(instance.email)
        instance.invite_code = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

    def get_verification_url(self, obj):
        return reverse("verify", kwargs={"key": obj.verification_key}, request=self.context['request'])

class TeamSerializer(serializers.ModelSerializer):
   # members = UserSerializer(many=True, read_only=True, default=[])
    class Meta:
        model = Team
        fields = ['name']

def generate_verification_key(email):
    salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
    email = email
    if isinstance(email, unicode):
        email = email.encode('utf-8')
        return hashlib.sha256(salt + email).hexdigest()[:32]
