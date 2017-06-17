### Dependencies
  * Python - 2.7.13 via pyenv (development) <https://github.com/pyenv/pyenv>
  * Postgresql
  * Django 1.11.x
  * httpie (for devlopment making api requests)

### Run Locally

```
git clone git@github.com:hindenbug/drf.git

cd drf

pip install -r requirements.txt

pip install httpie

python manage.py migrate --settings=i2x.settings.development

# run tests
python manage.py test --settings=i2x.settings.test

# run the server
python manage.py runserver --settings=i2x.settings.development
```

Application is now running on [http://localhost:8000]

### Deployment instructions (for heroku)

```
heroku login

heroku create

heroku config:set DISABLE_COLLECTSTATIC=1

git push heroku master

heroku ps:scale web=1

heroku run ./manage.py migrate api --settings=i2x.settings.production
```

## API Documentation

### POST /register/ <br/> POST /register/?code=someinvitecode

Register a new user via direct login or invitation code.

```
http POST https://stark-atoll-31508.herokuapp.com/register/ email=test@test.com password=12345678
```

Attribute    | Type      |
---------    | --------- |
**email**    | body (mandatory)   |
**password** | body (mandatory)   |
**code**     | url param (optional)|

##### Returns:

```
HTTP/1.1 201 Created
{
	"email": "test@test.com",
    "first_name": "",
    "last_name": "",
    "team": null,
    "verification_url": "https://stark-atoll-31508.herokuapp.com/verify/2880f13eaefc66be2a329deeb4867324/"
}
```

A verification link is being sent in the api response as no email feature is built.

##### Errors:
Error | Description
----- | ------------
400   | ```email/password``` is not present
409   | User already exists

Example:

```
{
    "email": [
        "This field is required."
    ]
}

```
```
{
    "email": [
        "user with this email already exists."
    ]
}
```

### POST /login

Login api to get the access token for making autheticated requests.

```
http POST https://stark-atoll-31508.herokuapp.com/login/ email=test@test.com password=12345678

```

Attribute      | Description
-------------- | -----------
**email**      | mandatory
**password**   | mandatory

##### Returns

```
HTTP/1.1 200 OK
{
    "token": "657e6eea6fef3ff375eb9511bcf6ccd20b86f03a"
}
```

##### Errors

Error | Description
----- | ------------
401   | Unauthorized (invalid email/password)


### POST /verify/:verification_key

Api to verify the user's registaration, this link is to be sent via email (in real world) for now is a
part of register api response.

```
http POST https://stark-atoll-31508.herokuapp.com/verify/2880f13eaefc66be2a329deeb4867324/
```

Returns

```
HTTP/1.0 200 OK
{
    "message": "Your account has been verified successfully."
}

```

#### Errors

Error | Description
----- | ------------
400   | Invalid verification url


### GET /reset/

Trigger a password reset for the user who requested it. Creates a new /password setup link with a
reset token.

```
# requires /login to get the token first

http GET https://stark-atoll-31508.herokuapp.com/reset/ \
> "Authorization: Token e5c9f0e70d908d53c01e2d7bc1cd63e4f0396418"
```

##### Returns

```
HTTP/1.0 200 OK

{
	"reset_password_link": "Here is you password reset link https://stark-atoll-31508.herokuapp.com/password/?token=e9b287aa162b488bbd4bc164f45b1ea7"
}

```

### POST /password/?token=password_reset_token

Sets up a new password for the user.

```
# requires /login to get the token first

http POST https://stark-atoll-31508.herokuapp.com/password/?token=7cee6503bd0f422495f0bf93692f3a59 \
> email=test12@test.com password=12345679 \
> "Authorization: Token e5c9f0e70d908d53c01e2d7bc1cd63e4f0396418"
```

#### Returns
```
HTTP/1.0 200 OK
{
    "message": "Your password was updated successfully!"
}
```
#### Errors

Error | Description
----- | ------------
400   | Invalid request. In case of a wrong password reset token


### POST /teams/

Api to create team for the user.

```
# requires /login to get the token first

http POST https://stark-atoll-31508.herokuapp.com/teams/ "Authorization: Token e5c9f0e70d908d53c01e2d7bc1cd63e4f0396418" \
> name="test"
```

Returns

```
HTTP/1.1 201 Created

{
   "name": "Team"
}
```

#### Errors

Error | Description
----- | ------------
400   | When the user already has a team created/User needs to be a member of a team before they can create one.


### GET /invite/

Api to invite other users. Generates a invitation link.

```
# requires /login to get the token first

http GET https://stark-atoll-31508.herokuapp.com/invite/ "Authorization: Token e5c9f0e70d908d53c01e2d7bc1cd63e4f0396418"
```

#### Returns

```
HTTP/1.0 200 OK
{
    "invite_link": " would like to invite you to join https://stark-atoll-31508.herokuapp.com/register/?code=QS1LYXae"
}
```

#### Errors

Error | Description
----- | ------------
400   | User needs to be a member of a team before they can share invite with others.


### Heroku Link
[Api](https://stark-atoll-31508.herokuapp.com/)
