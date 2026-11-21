# WasteWise — Phase 2: Ward-Level Analytics Plan

## Overview

Phase 2 extends WasteWise from a single-image classification tool into a comprehensive ward-level waste management analytics platform. This phase introduces geospatial tracking, temporal analysis, compliance scoring, and integration with municipal waste management systems.

## Objectives

1. **Ward-level segregation compliance monitoring**: Track segregation status across geographic wards using aggregated predictions from the segregation status classifier.
2. **Temporal trend analysis**: Monitor how segregation compliance changes over time — daily, weekly, monthly — to measure the impact of awareness campaigns and policy interventions.
3. **Geospatial visualization**: Display compliance metrics on interactive maps at the ward level, enabling administrators to identify hotspots of poor segregation.
4. **Automated reporting**: Generate weekly and monthly compliance reports for municipal authorities, including actionable insights and comparisons across wards.
5. **Feedback loop**: Provide ward-level feedback to sanitation workers and residents to encourage improvement.

## Architecture Extensions

### New Backend Components

- **Ward Model**: Database table for ward definitions (name, boundaries as GeoJSON, population, collection schedule).
- **Collection Point Model**: Database table linking collection points to wards (latitude, longitude, bin type, capacity).
- **Assessment Model**: Extended prediction record with collection point ID, ward ID, timestamp, and sanitation worker ID.
- **Analytics Service**: Computes ward-level metrics — compliance rate, trend direction, week-over-week change, ranking among wards.
- **Report Service**: Generates PDF/HTML reports from analytics data.
- **Geospatial API**: Endpoints for GeoJSON data, heatmaps, and ward boundary overlays.

### New API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/wards` | List all wards with current compliance scores |
| GET | `/api/v2/wards/{id}` | Detailed ward info with time-series data |
| GET | `/api/v2/wards/{id}/assessments` | All assessments for a ward |
| GET | `/api/v2/analytics/overview` | City-wide compliance dashboard data |
| GET | `/api/v2/analytics/trends` | Trend data over configurable time range |
| GET | `/api/v2/analytics/ranking` | Wards ranked by compliance rate |
| POST | `/api/v2/assessments` | Submit a new scene assessment with location |
| GET | `/api/v2/reports/weekly` | Generate weekly compliance report |

### New Frontend Components

- **Dashboard**: City-wide overview with key metrics — overall compliance rate, total assessments, top/bottom wards.
- **Map View**: Interactive map (Leaflet/MapBox) with ward boundaries coloured by compliance rate (green = high, red = low).
- **Ward Detail**: Drill-down view for a specific ward showing trend charts, recent assessments, and collection point statuses.
- **Report Viewer**: View and download generated reports.
- **Assessment Submission**: Mobile-friendly interface for sanitation workers to capture and submit scene photos with GPS location.

## Data Collection Strategy

### Sanitation Worker App

A simplified mobile-friendly web interface for sanitation workers to:
1. Open the camera and capture a photo of a waste collection point
2. GPS coordinates are automatically captured
3. The image is uploaded and classified automatically
4. The worker can override the classification if incorrect
5. The assessment is recorded with ward ID, collection point ID, timestamp, and worker ID

### Target Collection Volume

- **Daily**: 5–10 assessments per ward per day
- **Weekly**: 35–70 assessments per ward
- **Monthly**: 150–300 assessments per ward
- **Coverage**: At least 80% of collection points assessed per week

## Compliance Scoring

The ward compliance score is calculated as:

```
Compliance Rate = (Properly Segregated Assessments / Total Assessments) × 100
```

Ratings:
- **Excellent** (≥90%): Green
- **Good** (75–89%): Light Green
- **Moderate** (60–74%): Yellow
- **Poor** (40–59%): Orange
- **Critical** (<40%): Red

## Timeline

| Phase | Duration | Deliverables |
|-------|----------|-------------|
| 2.1 | 2 weeks | Ward/Collection Point database models, seed data |
| 2.2 | 2 weeks | Segregation status model training (requires annotated data) |
| 2.3 | 3 weeks | Analytics backend — compliance scoring, trends, ranking |
| 2.4 | 3 weeks | Frontend dashboard — map view, ward detail, charts |
| 2.5 | 2 weeks | Report generation and export |
| 2.6 | 2 weeks | Mobile assessment interface for field workers |
| 2.7 | 2 weeks | Testing, optimization, and pilot deployment |

**Total estimated duration**: 16 weeks

## Technical Requirements

- **Database**: Upgrade from SQLite to PostgreSQL for concurrent access and GeoJSON support
- **Mapping library**: Leaflet.js with OpenStreetMap tiles (free) or MapBox (requires API key)
- **Chart library**: Chart.js or Recharts for trend visualization
- **PDF generation**: WeasyPrint or ReportLab for server-side report generation
- **Geospatial**: PostGIS extension for spatial queries, or fallback to Python shapely library

## Privacy and Ethics

- Worker IDs should be anonymized in public-facing reports
- Assessment images should not contain identifiable personal information
- Compliance scores should be presented as improvement tools, not punitive measures
- Data retention policies should be defined in coordination with municipal authorities
