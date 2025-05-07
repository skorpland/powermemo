<div align="center">
    <a href="https://powermemo.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://assets.memodb.io/powermemo-dark.svg">
      <img alt="Shows the Powermemo logo" src="https://assets.memodb.io/powermemo-light.svg" width="424">
    </picture>
  </a>
  <p><strong>User Profile-Based Memory for GenAI Apps</strong></p>
  <p>
    <a href="https://www.npmjs.com/package/@powermemo/powermemo">
      <img src="https://img.shields.io/npm/v/@powermemo/powermemo.svg?logo=npm&&logoColor=fff&style=flat&colorA=2C2C2C&colorB=28CF8D">
    </a>
    <a href="https://jsr.io/@powermemo/powermemo">
      <img src="https://img.shields.io/jsr/v/@powermemo/powermemo.svg?logo=jsr&&logoColor=fff&style=flat&colorA=2C2C2C&colorB=28CF8D" />
    </a>
    <a href="https://npmcharts.com/compare/@powermemo/powermemo?minimal=true">
      <img src="https://img.shields.io/npm/dm/@powermemo/powermemo.svg?logo=typescript&&logoColor=fff&style=flat&colorA=2C2C2C&colorB=28CF8D" />
    </a>
    <a href="https://github.com/memodb-io/powermemo/actions/workflows/publish.yaml">
      <img src="https://github.com/memodb-io/powermemo/actions/workflows/publish.yaml/badge.svg">
    </a>
  </p>
</div>

# Powermemo TypeScript and JavaScript API Library
This library provides convenient access to the Powermemo REST API from TypeScript or JavaScript.


## Installation

```sh
npm install @powermemo/powermemo
```

### Installation from JSR

```sh
deno add jsr:@powermemo/powermemo
npx jsr add @powermemo/powermemo
```


## Usage

The code below shows how to get started using the completions API.

<!-- prettier-ignore -->
```js
import { PowerMemoClient, Blob, BlobType } from '@powermemo/powermemo';

const client = new PowerMemoClient(process.env['POWERMEMO_PROJECT_URL'], process.env['POWERMEMO_API_KEY'])

const main = async () => {
    const ping = await client.ping()
    console.log(ping)

    const config = await client.getConfig()
    console.log(config)

    const updateConfig = await client.updateConfig('a: 1')
    console.log(updateConfig)

    let userId = await client.addUser()
    console.log(userId)

    userId = await client.updateUser(userId, { name: 'John Doe' })
    console.log('Updated user id: ', userId)

    let user = await client.getUser(userId)
    console.log(user)

    const blobId = await user.insert(Blob.parse({
        type: BlobType.Enum.chat,
        messages: [{
            role: 'user',
            content: 'Hello, how are you? my name is John Doe'
        }]
    }))
    console.log(blobId)

    const blob = await user.get(blobId)
    console.log(blob)

    const flushSuc = await user.flush(BlobType.Enum.chat)
    console.log('Flush success: ', flushSuc)
    
    const blobs = await user.getAll(BlobType.Enum.chat)
    console.log(blobs)

    user = await client.getOrCreateUser(userId)
    console.log(user)

    const profiles = await user.profile(2000, ['Topic1'], ['SubTopic1'], 200, { Topic1: 200 })
    console.log(profiles)

    const event = await user.event(10, 1000)
    console.log(event)

    const context = await user.context(2000, 1000)
    console.log(context)

    profiles.map((profile) => {
        user.deleteProfile(profile.id).then((isDel) => {
            console.log('Delete profile success: ', isDel)
        })
    })

    const isDel = await client.deleteUser(userId)
    console.log(isDel)
}

main()
```

## Support

Join the community for support and discussions:

-  [Join our Discord](https://discord.gg/YdgwU4d9NB) 👻 

-  [Follow us on Twitter](https://x.com/powermemo_io) 𝕏 

Or Just [email us](mailto:contact@powermemo.io) ❤️


## Contributors

This project exists thanks to all the people who contribute.

And thank you to all our backers! 🙏

<a href="https://github.com/memodb-io/powermemo/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=memodb-io/powermemo" />
</a>


## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](https://github.com/memodb-io/powermemo/blob/main/LICENSE) file for details.