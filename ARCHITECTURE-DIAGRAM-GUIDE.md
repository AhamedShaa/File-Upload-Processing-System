# Architecture Diagram Placeholder

## 📐 Add Your Architecture Diagram Here

Your architecture diagram should be placed in the root directory as:
- **Filename:** `architecture-diagram.png`
- **Format:** PNG, JPG, or SVG
- **Recommended size:** 1200x800 pixels
- **Tools to create diagram:** Lucidchart, Draw.io, Figma, Miro, or ArchiMate

## 🏗️ What Your Diagram Should Show

Your architecture diagram should illustrate these components and flows:

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Architecture                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │   Client     │────────▶│ API Gateway  │                  │
│  │  (Web/App)   │         └──────┬───────┘                  │
│  └──────────────┘                │                          │
│                                  │                          │
│                    ┌─────────────┴──────────────┐            │
│                    ▼                            ▼            │
│            ┌──────────────┐          ┌──────────────┐       │
│            │  Presign     │          │  Status      │       │
│            │  Lambda      │          │  Lambda      │       │
│            └──────┬───────┘          └──────┬───────┘       │
│                   │                         │                │
│                   ▼                         ▼                │
│         ┌────────────────┐      ┌──────────────────┐        │
│         │  S3 Raw Files  │      │   DynamoDB       │        │
│         │  (uploads)     │      │   Jobs Table     │        │
│         └────────┬───────┘      └──────────────────┘        │
│                  │                                           │
│                  │ (S3 Event)                               │
│                  ▼                                           │
│         ┌──────────────┐                                    │
│         │    SQS       │                                    │
│         │   Queue      │                                    │
│         └──────┬───────┘                                    │
│                │ (Message)                                  │
│                ▼                                            │
│         ┌──────────────┐                                    │
│         │ Processor    │                                    │
│         │ Lambda       │                                    │
│         │ (PIL/Python) │                                    │
│         └──────┬───────┘                                    │
│                │                                            │
│                ▼                                            │
│      ┌──────────────────┐                                  │
│      │ S3 Processed     │                                  │
│      │ (large, thumb)   │                                  │
│      └──────────────────┘                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Components to Include

### Inputs
- Client Application
- REST API Endpoints

### Processing Services  
- Lambda Functions (Presign, Processor, Status)
- Terraform Infrastructure Code

### Storage
- S3 Buckets (Raw & Processed)
- DynamoDB Table

### Messaging & Events
- SQS Queue
- S3 Event Notifications
- Lambda Event Sources

### Monitoring
- CloudWatch Logs
- CloudWatch Metrics

## 🎨 Design Recommendations

1. **Color Coding:**
   - Blue for API & networking
   - Orange for compute (Lambda)
   - Green for storage (S3, DynamoDB)
   - Purple for messaging (SQS)
   - Gray for monitoring

2. **Show Data Flow:**
   - Solid arrows for synchronous calls
   - Dashed arrows for asynchronous events
   - Label arrows with data types

3. **Annotations:**
   - Include service names
   - Show request/response types
   - Indicate processing stages

## 🔗 Tools to Create Diagram

- **Lucidchart:** https://www.lucidchart.com (AWS shapes available)
- **Draw.io:** https://draw.io (Free, online)
- **Figma:** https://figma.com (Collaborative design)
- **AWS Architecture Icons:** Download from AWS
- **Miro:** https://miro.com (Great for teams)

## 📝 After Creating Your Diagram

1. Export as PNG or JPG (recommended: PNG for clarity)
2. Save as `architecture-diagram.png` in project root
3. Commit and push to GitHub:
   ```bash
   git add architecture-diagram.png
   git commit -m "Add architecture diagram"
   git push
   ```

## ✅ Diagram Checklist

- [ ] All major AWS services shown
- [ ] Data flow clearly indicated
- [ ] Component relationships clear
- [ ] File uploaded as `architecture-diagram.png`
- [ ] High resolution (preferably 1200px+ width)
- [ ] Professional appearance
- [ ] Committed to git

Once you've added your diagram, the README.md will automatically display it in the Overview section!

---

**Need help creating the diagram?** Check out these resources:
- AWS Architecture Best Practices: https://docs.aws.amazon.com/whitepapers/
- Serverless Architecture Patterns: https://www.serverless.com
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
