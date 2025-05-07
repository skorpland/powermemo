# PowerMemo Go Client

A Go client library for interacting with the PowerMemo API. This library allows you to store, retrieve, and manage chat conversation data in PowerMemo.

## Installation

```bash
go get github.com/skorpland/powermemo/src/client/powermemo-go
```

## Requirements

- Go 1.22.3 or higher
- A PowerMemo project URL and API key

## Usage

### Initialize the Client

```go
import (
    "github.com/skorpland/powermemo/src/client/powermemo-go/core"
)

// Initialize with direct API key
client, err := core.NewPowerMemoClient(
    "YOUR_PROJECT_URL",
    "YOUR_API_KEY",
)

// Or using environment variable POWERMEMO_API_KEY
client, err := core.NewPowerMemoClient(
    "YOUR_PROJECT_URL",
    "",  // Will use POWERMEMO_API_KEY environment variable
)
```

### Managing Users

```go
// Create or get a user with UUID
import "github.com/google/uuid"

userid := uuid.New()
user, err := client.GetOrCreateUser(userid.String())

// Get user
user, err := client.GetUser(userid.String(), false)

// Delete user
err := client.DeleteUser(userid.String())
```

### Working with Chat Blobs

PowerMemo currently supports `ChatBlob` for storing conversation messages.

#### Chat Blob Example

```go
import (
    "github.com/skorpland/powermemo/src/client/powermemo-go/blob"
)

// Create a chat blob
chatBlob := &blob.ChatBlob{
    BaseBlob: blob.BaseBlob{
        Type: blob.ChatType,
    },
    Messages: []blob.OpenAICompatibleMessage{
        {
            Role:    "user",
            Content: "Hello, I am Jinjia!",
        },
        {
            Role:    "assistant",
            Content: "Hi there! How can I help you today?",
        },
    },
}

// Insert the blob
blobID, err := user.Insert(chatBlob)

// Retrieve the blob
retrievedBlob, err := user.Get(blobID)
chatBlob, ok := retrievedBlob.(*blob.ChatBlob)

// Get all chat blobs (with pagination: offset, limit)
blobIDs, err := user.GetAll(blob.ChatType, 0, 10)
```

### User Profiles

```go
// Flush blobs to update profiles
user.Flush(blob.ChatType)

// Get user profiles
profiles, err := user.Profile()

// Delete a profile
err = user.DeleteProfile(profileID)
```

## Blob Types

The library currently supports:

- `blob.ChatType`: For chat conversations

## Complete Example

For a complete working example of how to use the PowerMemo Go client, see [examples/main.go](examples/main.go) in the repository.

## License

This project is licensed under the terms of the license provided with the PowerMemo project.
