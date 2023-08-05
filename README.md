# AI Chat Service

## Main chat endpoint
POST api/v1/chat

Headers:
Content-Type: application/json
Authorization: Api-Key <API_KEY>

Body:
{
  "message": "test3",
  "context": [
    {
      "message": "Hello world",
      "type": "bot"
    },
    {
      "message": "example query",
      "type": "user"
    },
    {
      "message": "example AI chat response",
      "type": "bot"
    },
  ]
}