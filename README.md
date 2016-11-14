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
The lists endpoint can be accessed on `/lists`. This endpoint will return an object containing an array of the lists that are currently monitored by Luath with the details about each list.

```
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "swift-corelibs-dev",
      "email": "swift-corelibs-dev@swift.org",
      "description": "Discussion of the implementation of the Swift core libraries."
    }
  ...
  ]
}
```

### Messages
You can get the messages in a list by querying the `messages` resource. Messages in a list are available under `/lists/{list-id}/messages`. This returns a list of messages and their associated data.

```
{
  "count": 918,
  "next": "http://www.luath.org/api/v1/lists/1/messages?limit=100&offset=100",
  "previous": null,
  "results": [
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
}
...
```

### Message Details
You can get the messages in a list by querying the `messages` resource. Message details are available by querying the messages endpoint with a message id. For example: `/lists/{list-id}/messages/{message-id}`. This returns the message details.

```
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
```

### Pagination
The `messages` endpoint is paginated, and you can read different pages by providing an `offset` query parameter. You can also provide a `limit` parameter, but it is optional and the default limit is 100 messages. If you don't provide or provide an invalid `offset` the API will return the first page (offset 0, limit 100).

### Response Codes
You can expect all successful response codes to be `200`. If there is an error, you will receive a `500` with a message detailing the error, if there are any details. If you don't provide an authorization token, or the token is not valid, you will receive a `401` response.

# Contributing
Thanks for thinking about contributing to Luath. If you'd like to help out, open an issue so we can talk about what you're wanting to do, and when we've fleshed out the details, I'll be happy to look at a pull request.

# License
This project is licensed under the MIT License - see the LICENSE.md file for details
