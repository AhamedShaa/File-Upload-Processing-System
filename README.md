# File Upload + Processing System

A scalable, serverless file upload and image processing system built with AWS Lambda, S3, DynamoDB, and API Gateway. Upload images and automatically generate resized versions and thumbnails.

## 📋 Overview

This project demonstrates a production-ready file processing pipeline that:
- Accepts file uploads via secure presigned URLs
- Automatically triggers image processing on upload
- Resizes images to multiple formats (large, thumbnail)
- Tracks job status with DynamoDB
- Exposes REST APIs for upload, status checking, and retrieval

## 🏗️ Architecture

![Architecture Diagram](./architecture-diagram.png)

### Components

| Component | Purpose |
|-----------|---------|
| **API Gateway** | REST endpoints for upload requests and status checks |
| **Lambda - Presign** | Generates secure, time-limited S3 presigned URLs |
| **Lambda - Processor** | Processes uploaded images (resize, optimize) |
| **Lambda - Status** | Retrieves job status and output information |
| **S3 (Input)** | Stores raw uploaded images |
| **S3 (Output)** | Stores processed images (large, thumbnails) |
| **DynamoDB** | Maintains job metadata and processing status |
| **SQS** | Buffers S3 events for reliable processing |

## ✨ Features

- ✅ **Secure Upload**: Presigned URLs with 5-minute expiry
- ✅ **Multi-format Output**: Large (1200px) and thumbnail (200px) versions
- ✅ **Job Tracking**: Real-time status updates via DynamoDB
- ✅ **Automatic Processing**: S3 events trigger Lambda processors
- ✅ **Error Handling**: Comprehensive error tracking and logging
- ✅ **CORS Support**: Cross-origin requests enabled for web clients
- ✅ **Infrastructure as Code**: Complete Terraform configuration
- ✅ **Scalable**: Serverless architecture handles variable loads

## 📦 Prerequisites

- **AWS Account** with appropriate permissions
- **AWS CLI** configured with credentials
- **Terraform** >= 1.0
- **Python** 3.9+
- **Pillow (PIL)** for image processing

### Required IAM Permissions

- S3: CreateBucket, GetObject, PutObject
- Lambda: CreateFunction, InvokeFunction
- DynamoDB: CreateTable, PutItem, UpdateItem, GetItem
- API Gateway: CreateRestApi, CreateDeployment
- CloudWatch: CreateLogGroup, CreateLogStream
- SQS: CreateQueue, ReceiveMessage, DeleteMessage

## 📂 Project Structure

```
file-processor/
├── README.md                    # Project documentation
├── architecture-diagram.png     # Architecture diagram (add your PNG here)
├── job.json                     # Example job response
├── response.json                # Example API response
├── test_upload.py               # Integration test script
│
├── lambdas/
│   ├── presign/
│   │   └── lambda_function.py   # Generates presigned upload URLs
│   ├── processor/
│   │   ├── lambda_function.py   # Processes images (resize, thumbnail)
│   │   └── PIL/                 # Pillow library bundle for Lambda
│   └── status/
│       └── lambda_function.py   # Checks job status
│
└── terraform/
    ├── main.tf                  # Infrastructure as Code
    └── terraform.tfstate*       # State files (generated)
```

## 🚀 Quick Start

### 1. Clone & Navigate

```bash
git clone https://github.com/AhamedShaa/File-Upload-Processing-System.git
cd file-processor
```

### 2. Deploy with Terraform

```bash
cd terraform
terraform init          # Initialize Terraform
terraform plan          # Review planned changes
terraform apply         # Deploy infrastructure
```

Terraform will create:
- 2 S3 buckets (input & processed)
- 3 Lambda functions (presign, processor, status)
- 1 DynamoDB table (jobs metadata)
- 1 API Gateway with endpoints

### 3. Get API Endpoint

```bash
cd terraform
terraform output api_endpoint
```

## 📡 API Endpoints

### 1. **Upload Presigned URL**
Generate a secure upload URL for your file.

```bash
curl -X POST https://your-api-endpoint/upload \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "photo.jpg",
    "contentType": "image/jpeg"
  }'
```

**Response:**
```json
{
  "jobId": "fb5d2bbd-a0ec-4464-9560-342fa79566b6",
  "uploadUrl": "https://file-processor-raw-a3f9.s3.amazonaws.com/uploads/...",
  "s3Key": "uploads/fb5d2bbd-a0ec-4464-9560-342fa79566b6/photo.jpg"
}
```

### 2. **Check Job Status**
Monitor processing progress.

```bash
curl -X GET https://your-api-endpoint/status/{jobId}
```

**Response:**
```json
{
  "jobId": "fb5d2bbd-a0ec-4464-9560-342fa79566b6",
  "status": "DONE",
  "filename": "photo.jpg",
  "createdAt": "1776834461.7466197",
  "processedAt": "1776834466.0247755",
  "outputKeys": {
    "large": "processed/large/fb5d2bbd.../photo.jpg",
    "thumbnail": "processed/thumbnail/fb5d2bbd.../photo.jpg"
  }
}
```

## 💻 Usage Example

See [test_upload.py](./test_upload.py) for a complete example:

```python
import requests
import json
import time

API_URL = "https://your-api-endpoint"

# Step 1: Get presigned URL
response = requests.post(
    f"{API_URL}/upload",
    json={"filename": "photo.jpg", "contentType": "image/jpeg"}
)
body = response.json()
job_id = body['jobId']

# Step 2: Upload file directly to S3
with open('photo.jpg', 'rb') as f:
    upload_response = requests.put(
        body['uploadUrl'],
        data=f,
        headers={'Content-Type': 'image/jpeg'}
    )

# Step 3: Check status
time.sleep(5)  # Wait for processing
status_response = requests.get(f"{API_URL}/status/{job_id}")
print(json.dumps(status_response.json(), indent=2))
```

## 🔄 Data Flow

1. **User submits upload request** → API Gateway receives filename
2. **Presign Lambda** → Generates presigned URL, creates job record
3. **User uploads file** → Direct S3 upload using presigned URL
4. **S3 event triggers** → SQS receives notification
5. **Processor Lambda** → Consumes queue, processes image
6. **Resized images saved** → Output S3 bucket
7. **DynamoDB updated** → Job status changed to DONE
8. **User checks status** → Status Lambda retrieves job info

## 📊 Job Status States

| Status | Meaning |
|--------|---------|
| `PENDING` | Upload URL generated, awaiting file upload |
| `PROCESSING` | Image received, resizing in progress |
| `DONE` | All versions processed, ready for download |
| `FAILED` | Processing error occurred |

## 🛠️ Configuration

Environment variables set by Terraform:

```env
INPUT_BUCKET=file-processor-raw-a3f9
OUTPUT_BUCKET=file-processor-processed-a3f9
JOBS_TABLE=file-processor-jobs
URL_EXPIRY=300  # seconds
```

### Image Processing Sizes

Configure in `lambdas/processor/lambda_function.py`:

```python
SIZES = [
    ('large',     1200),      # 1200px width
    ('thumbnail', 200),       # 200px width
]
```

## 🔐 Security Features

- ✅ **Presigned URLs**: Time-limited (5 minutes), single-use
- ✅ **S3 Block Public Access**: All buckets are private
- ✅ **IAM Roles**: Least privilege principle
- ✅ **Input Validation**: Filename and content-type checks
- ✅ **CORS Headers**: Restricted origins (configurable)
- ✅ **DynamoDB TTL**: Auto-expiry of old job records

## 📈 Scaling Considerations

**Current Setup (Development):**
- Lambda concurrency: 100 (default)
- S3: Unlimited requests
- DynamoDB: On-demand pricing

**Production Improvements:**
- Add SQS for buffering (already configured in processor)
- Set Lambda concurrency limits to prevent runaway costs
- Enable DynamoDB point-in-time recovery
- Add S3 object lifecycle policies
- Implement CloudWatch alarms
- Enable VPC endpoints for private connectivity

## 🧪 Testing

Run the integration test:

```bash
python test_upload.py
```

Replace the API endpoint in the script with your actual endpoint.

## 📝 Monitoring

### CloudWatch Logs

View Lambda execution logs:

```bash
aws logs tail /aws/lambda/file-processor-presign --follow
aws logs tail /aws/lambda/file-processor-processor --follow
aws logs tail /aws/lambda/file-processor-status --follow
```

### DynamoDB Metrics

Monitor table metrics:

```bash
aws cloudwatch list-metrics --namespace AWS/DynamoDB --dimensions Name=TableName,Value=file-processor-jobs
```

## 🧹 Cleanup

Destroy all AWS resources:

```bash
cd terraform
terraform destroy
```

⚠️ **Warning**: This will delete all S3 buckets, tables, and functions. Data cannot be recovered.

## 🚀 Future Enhancements

- [ ] Add video processing support
- [ ] Implement image format conversion (WebP, AVIF)
- [ ] Add watermarking capability
- [ ] Batch processing API
- [ ] Web UI dashboard
- [ ] Cost optimization analysis
- [ ] Advanced image filters
- [ ] CDN integration (CloudFront)

## 📚 Technologies Used

- **AWS Services**: Lambda, S3, DynamoDB, API Gateway, SQS, CloudWatch
- **Languages**: Python 3.9+
- **Libraries**: Pillow (image processing), Boto3 (AWS SDK)
- **IaC**: Terraform
- **Testing**: Python requests, boto3

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ahamed Shaa**  
GitHub: [@AhamedShaa](https://github.com/AhamedShaa)

## 📞 Support

- Open an issue for bugs or feature requests
- Check [examples](./examples/) for additional use cases
- Review AWS Lambda best practices: https://docs.aws.amazon.com/lambda/

## 🙏 Acknowledgments

- AWS Lambda & Serverless Architecture
- Pillow Image Library
- Terraform Infrastructure as Code
- Open Source Community

---

**Last Updated:** April 2026  
**Project Status:** Production Ready ✅
