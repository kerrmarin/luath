# Luath Project
Luath is a web service that allows you to query for details of emails from the Swift Mailing Lists.

# Components
The Luath project has three main components:

- The API
- The email importer
- The Luath homepage

# Usage
If you haven't yet, head over to [the Luath homepage](http://www.luath.org) and request an API key. Once you're set with an API key you can start querying the Luath API.

The Luath API is available at `http://www.luath.org/api/v1`.

## Authentication
Once you have your API key, each request you make will have to have that key in the `Authorization` header. So if I were to make a request, one of the headers for the request would, for example, be:

```
Authorization: Token bkayZOMvuy8aZOhIgxq94K9Oe7Y70Hw55
```

## Endpoints
There are currently three endpoints for the Luath API.

### Lists
The lists endpoint can be accessed on `/lists`. This endpoint will return an array of the lists that are currently monitored by Luath with the details about each list.

```
[
  {
    "id": 1,
    "name": "swift-corelibs-dev",
    "email": "swift-corelibs-dev@swift.org",
    "description": "Discussion of the implementation of the Swift core libraries."
  }
  ...
]
```

### Messages
You can get the messages in a list by querying the `messages` resource. Messages in a list are available under `/lists/{list-id}/messages`. This returns a list of messages and their associated data. You must pass in a limit and an offset for this endpoint as query strings.

```
[
  {
    "id": "0040B915-CB9C-4D8E-9BAA-79FC3FE4B03D@jelee.co.uk",
    "from": "james@jelee.co.uk",
    "from_name": "James Lee",
    "in_reply_to": null,
    "date": "2015-12-08T12:23:19.000Z",
    "datestring": "Tue, 8 Dec 2015 12:23:19 +0000",
    "subject": "[swift-corelibs-dev] NSAttributedString attributesAtIndex return an\n\toptional.",
    "content": "Hi all,\n\nBeen playing around with NSAttributedString ...",
    "listId": 1
  }
]
...
```

### Search (Not yet implemented)
You can search the Luath database in the subject or content fields for a query. The search endpoint is available under `/search/{list-id}/{query}`. You must also pass in a limit and offset to this endpoint. This endpoint returns a list of objects containing the message ID that matches your query.

```
[
  {
    "messageId": "9D39DBB5-FF05-42ED-BF0A-D45C69B1AFE7@me.com"
  }
  ...
]
```

### Response Codes
You can expect all successful response codes to be `200`. If there is an error, you will receive a `500` with a message detailing the error, if there are any details. If there is an error in the input you provided, you will receive a `403` status code with a message detailing what the expected inputs are.

# Contributing
Thanks for thinking about contributing to Luath. If you'd like to help out, open an issue so we can talk about what you're wanting to do, and when we've fleshed out the details, I'll be happy to look at a pull request.

# License
This project is licensed under the MIT License - see the LICENSE.md file for details
