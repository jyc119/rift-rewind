import {
  BedrockRuntimeClient,
  InvokeModelCommand,
} from "@aws-sdk/client-bedrock-runtime";

const client = new BedrockRuntimeClient({ region: "us-east-1" });

async function testBedrock() {
  const prompt =
    "Give me a short motivational message for a League of Legends player";
  const input = {
    prompt,
    max_tokens: 100,
  };

  const command = new InvokeModelCommand({
    modelId: "anthropic.claude-sonnet-4-20250514-v1:0",
    contentType: "application/json",
    accept: "application/json",
    body: JSON.stringify(input),
  });

  const response = await client.send(command);
  const text = new TextDecoder().decode(
    await response.body.transformToByteArray()
  );
  console.log("Bedrock response: ", text);
}

testBedrock();
