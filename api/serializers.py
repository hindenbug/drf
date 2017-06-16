from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import User, Team
from .utils import generate_verification_key

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    verification_url = serializers.SerializerMethodField(read_only=True)
    code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'team', 'password', 'verification_url', 'code']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        invitee_code = validated_data.pop('code', None)
        invitee = User.objects.get(invite_code=invitee_code) if invitee_code else None
        instance = User(**validated_data)
        instance.verification_key = generate_verification_key(instance.email)
        instance.invite_code = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
        instance.team = invitee.team if invitee else None
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
