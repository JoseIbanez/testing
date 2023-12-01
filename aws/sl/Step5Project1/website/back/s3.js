import dotenv from 'dotenv'
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { S3Client, PutObjectCommand} from "@aws-sdk/client-s3";
import crypto from 'crypto'
import { promisify } from "util"
const randomBytes = promisify(crypto.randomBytes)

dotenv.config()

const region = "us-east-1"
const bucketName = process.env.BUCKETNAME



export async function generateUploadURL() {
  const rawBytes = await randomBytes(16)
  const imageName = rawBytes.toString('hex')

  console.log(bucketName)

  console.log("name:"+imageName)

  const params = ({
    Bucket: bucketName,
    Key: imageName,
  })
  
  const client = new S3Client({ region: 'us-east-1' })
  const command = new PutObjectCommand(params);
  const uploadURL = await getSignedUrl(client, command, { expiresIn: 3600 });

  console.log("uploadURL:"+uploadURL)
  return uploadURL
}