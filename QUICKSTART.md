# Quick Start Guide

Get the File Upload + Processing System running in 5 minutes!

## 1️⃣ Clone Repository

```bash
git clone https://github.com/AhamedShaa/File-Upload-Processing-System.git
cd file-processor
```

## 2️⃣ Install Terraform

```bash
# macOS (using Homebrew)
brew install terraform

# Windows (using Chocolatey)
choco install terraform

# Or download from: https://www.terraform.io/downloads.html
```

## 3️⃣ Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json
```

## 4️⃣ Deploy Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Type `yes` when prompted. Deployment takes ~2 minutes.

## 5️⃣ Get Your API URL

```bash
terraform output api_endpoint
```

Copy the URL - you'll need this for uploads!

## 6️⃣ Test Upload

### Option A: Use Python Script

```bash
# Edit test_upload.py with your API endpoint
nano test_upload.py  # Change API_URL

# Run the test
python test_upload.py
```

### Option B: Use cURL

```bash
API="https://your-api-endpoint-here"
FILE="path/to/image.jpg"

# Get upload URL
RESPONSE=$(curl -s -X POST $API/upload \
  -H "Content-Type: application/json" \
  -d '{"filename":"test.jpg","contentType":"image/jpeg"}')

JOB_ID=$(echo $RESPONSE | jq -r '.jobId')
UPLOAD_URL=$(echo $RESPONSE | jq -r '.uploadUrl')

echo "Job ID: $JOB_ID"

# Upload file
curl -X PUT "$UPLOAD_URL" --data-binary @"$FILE" -H "Content-Type: image/jpeg"

# Check status after 5 seconds
sleep 5
curl $API/status/$JOB_ID | jq .
```

## ✅ What Gets Created

| Service | Purpose | Cost |
|---------|---------|------|
| **S3 Buckets (2)** | Store raw and processed images | ~$0.023/GB |
| **Lambda (3)** | Process uploads and generate thumbnails | $0.20 per 1M requests |
| **DynamoDB** | Track job status | On-demand pricing |
| **API Gateway** | REST endpoints | $3.50 per million calls |
| **CloudWatch** | Monitoring and logs | ~$0.50/GB |

**Estimated monthly cost for light usage: $1-5**

## 🧹 Cleanup (Stop Charges)

```bash
cd terraform
terraform destroy
```

Type `yes` to confirm deletion.

## 🚀 Next Steps

1. **Add custom image sizes** - Edit `lambdas/processor/lambda_function.py`
2. **Deploy web UI** - Create HTML form for file uploads
3. **Add image filters** - Implement additional processing
4. **Set up domain** - Use Route53 + CloudFront
5. **Enable CORS** - For cross-origin requests

## 📚 Detailed Documentation

- **[README.md](./README.md)** - Full project overview
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Step-by-step deployment guide
- **[test_upload.py](./test_upload.py)** - Complete example code

## 🆘 Troubleshooting

**"terraform: command not found"**
```bash
# Install Terraform
# macOS: brew install terraform
# Ubuntu: sudo apt-get install terraform
```

**"AWS credentials not configured"**
```bash
aws configure
# Enter your credentials from AWS Console
```

**"Upload URL expired"**
- Presigned URLs last 5 minutes
- Get a new URL by calling the upload endpoint again

**"Image not processing"**
- Check CloudWatch logs: `aws logs tail /aws/lambda/file-processor-processor`
- Verify SQS is triggering Lambda
- Ensure S3 event notifications are enabled

## 💡 Tips

- Test with small images first (< 5 MB)
- Monitor CloudWatch for errors
- Set AWS budget alerts to prevent surprise charges
- Use S3 lifecycle policies to delete old uploads
- Keep Terraform state file safe (don't commit to git)

## 📞 Need Help?

- GitHub Issues: https://github.com/AhamedShaa/File-Upload-Processing-System/issues
- AWS Documentation: https://docs.aws.amazon.com
- Terraform Docs: https://www.terraform.io/docs

---

**Happy uploading!** 📸
