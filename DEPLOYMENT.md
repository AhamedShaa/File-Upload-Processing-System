# Deployment Guide

This guide walks you through deploying the File Upload + Processing System to AWS.

## Prerequisites

Before you start, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
   ```bash
   aws --version
   # Configure credentials
   aws configure
   ```
3. **Terraform** installed (>= 1.0)
   ```bash
   terraform --version
   ```
4. **Python 3.9+** installed
5. **Git** for version control

## Step 1: Clone the Repository

```bash
git clone https://github.com/AhamedShaa/File-Upload-Processing-System.git
cd file-processor
```

## Step 2: Prepare Lambda Dependencies

The processor Lambda needs Pillow for image resizing. Build dependencies locally:

```bash
cd lambdas/processor

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies into current directory (for Lambda packaging)
pip install -r requirements.txt -t .

# Deactivate virtual environment
deactivate
```

**Note:** The PIL library is large but necessary for image processing in Lambda.

## Step 3: Deploy with Terraform

```bash
cd terraform

# Initialize Terraform (downloads required providers)
terraform init

# Review planned infrastructure changes
terraform plan

# Deploy resources (will prompt for confirmation)
terraform apply
```

This creates:
- ✅ S3 bucket for raw uploads: `file-processor-raw-*`
- ✅ S3 bucket for processed images: `file-processor-processed-*`
- ✅ DynamoDB table for job tracking: `file-processor-jobs`
- ✅ 3 Lambda functions (presign, processor, status)
- ✅ API Gateway with REST endpoints
- ✅ SQS queue for reliable event processing
- ✅ CloudWatch logs for monitoring

## Step 4: Get Your API Endpoint

After deployment completes, get your API endpoint:

```bash
terraform output api_endpoint
```

Example output:
```
https://abc123def.execute-api.us-east-1.amazonaws.com/prod
```

## Step 5: Test the System

### Method 1: Using Python (Recommended)

```bash
# Update test_upload.py with your API endpoint
vim test_upload.py  # or edit with your editor

# Replace API_URL with your endpoint
API_URL = "https://your-api-endpoint"

# Run the test
python test_upload.py
```

### Method 2: Using cURL

```bash
# Get presigned URL
curl -X POST https://your-api-endpoint/upload \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "photo.jpg",
    "contentType": "image/jpeg"
  }'

# Save the jobId and uploadUrl from response
# Then upload your image:
curl -X PUT "YOUR_UPLOAD_URL" \
  --data-binary @photo.jpg \
  -H "Content-Type: image/jpeg"

# Check status:
curl https://your-api-endpoint/status/YOUR_JOB_ID
```

## Step 6: View Processed Images

After a successful upload and processing:

1. Go to AWS Console → S3
2. Open the `file-processor-processed-*` bucket
3. Navigate to `processed/large/` or `processed/thumbnail/`
4. Download your processed images

## Monitoring & Troubleshooting

### View Lambda Logs

```bash
# Presign Lambda
aws logs tail /aws/lambda/file-processor-presign --follow

# Processor Lambda
aws logs tail /aws/lambda/file-processor-processor --follow

# Status Lambda
aws logs tail /aws/lambda/file-processor-status --follow
```

### Check DynamoDB Table

```bash
aws dynamodb scan --table-name file-processor-jobs
```

### Common Issues

| Issue | Solution |
|-------|----------|
| 403 Forbidden on upload | Check S3 bucket policies and IAM permissions |
| 504 Gateway Timeout | Lambda may be slow; check logs and increase timeout in Terraform |
| Processing never completes | Verify SQS is connected to processor Lambda; check event source mappings |
| Large file upload fails | Increase `postBuffer` in git config: `git config http.postBuffer 524288000` |

## Configuration

### Adjust Image Sizes

Edit `lambdas/processor/lambda_function.py`:

```python
SIZES = [
    ('large',     1200),      # Change width here
    ('thumbnail', 200),       # Change width here
    ('medium',    800),       # Add new size if needed
]
```

Then redeploy:

```bash
cd terraform
terraform apply
```

### Change URL Expiry

Edit `lambdas/presign/lambda_function.py`:

```python
URL_EXPIRY = 300  # Change from 5 minutes to desired seconds
```

## Cost Optimization

To minimize AWS costs:

1. **Set DynamoDB TTL** - Auto-delete old job records
2. **Use S3 Lifecycle Policies** - Archive/delete old images
3. **Monitor with CloudWatch** - Set budget alerts
4. **Consider Reserved Capacity** - For production workloads

## Production Deployment Checklist

- [ ] Enable S3 versioning and MFA delete
- [ ] Set up CloudTrail for audit logging
- [ ] Enable Lambda reserved concurrency limits
- [ ] Configure DynamoDB point-in-time recovery
- [ ] Set up CloudWatch alarms for errors
- [ ] Use VPC endpoints for private connectivity
- [ ] Enable API Gateway caching
- [ ] Set up WAF rules for API protection
- [ ] Configure CloudFront CDN for processed images
- [ ] Enable Lambda X-Ray tracing for debugging

## Cleanup

To destroy all resources and avoid charges:

```bash
cd terraform
terraform destroy
```

⚠️ **Warning**: This is irreversible! All data will be deleted.

## Support

For issues or questions:
1. Check CloudWatch logs
2. Review AWS Lambda limits and quotas
3. Check repository issues: https://github.com/AhamedShaa/File-Upload-Processing-System/issues
4. Refer to AWS documentation: https://docs.aws.amazon.com/lambda/

## Next Steps

- Add image filters and effects
- Implement batch processing
- Create web UI dashboard
- Add video processing support
- Set up CI/CD pipeline

---

Happy deploying! 🚀
