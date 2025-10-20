import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import fs from "fs";

const s3 = new S3Client({ region: "us-east-1" });
const bucket = "rift-rewind-bucket";

async function upload() {
  const file = fs.readFileSync("test.txt");
  await s3.send(
    new PutObjectCommand({ Bucket: bucket, Key: "test.txt", Body: file })
  );
  console.log("Uploaded test.txt");
}

async function download() {
  const { Body } = await s3.send(
    new GetObjectCommand({ Bucket: bucket, Key: "test.txt" })
  );
  const data = await Body.transformToString();
  console.log("Downloaded: ", data);
}

await upload();
await download();
