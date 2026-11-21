# WasteWise — Project Overview

## Abstract

WasteWise is a deep-learning-powered waste management platform designed to assist households, municipal bodies, and waste management operators in classifying and segregating waste more effectively. By leveraging transfer learning with MobileNetV2, WasteWise provides real-time classification of waste items into Wet (organic/biodegradable) and Dry (recyclable/non-biodegradable) categories through a simple image upload interface. The system also supports a secondary model for assessing whether waste in a given scene has been properly segregated, enabling scalable monitoring of waste management compliance.

India generates over 150,000 tonnes of municipal solid waste daily, yet segregation at source remains inconsistent across most urban local bodies. WasteWise addresses this gap by providing an accessible, AI-driven tool that can be deployed as a web application, integrated into existing waste management workflows, or used as a standalone assessment tool by sanitation workers and citizens alike.

## Problem Statement

Improper waste segregation is a critical challenge in urban waste management across India and other developing nations. When wet and dry waste are mixed at the source, the downstream processing becomes significantly more expensive and environmentally damaging. Landfills receive unsegregated waste that could otherwise be composted (wet waste) or recycled (dry waste), leading to increased methane emissions, groundwater contamination, and loss of valuable recyclable materials.

Current segregation monitoring is entirely manual — sanitation inspectors visually check waste bins, which is labour-intensive, inconsistent, and unscalable. There is no automated system widely available to either classify individual waste items or assess the segregation quality of waste collection points.

The key challenges this project addresses are:
1. **Individual item classification**: Given an image of a single waste item, determine whether it is wet or dry waste.
2. **Segregation assessment** (Phase 2): Given an image of a waste bin or collection scene, assess whether the waste has been properly segregated.
3. **Accessibility**: The solution must work through a simple web interface without requiring specialized hardware for inference.

## Objectives

1. **Build a Wet/Dry classifier** using MobileNetV2 transfer learning, trained on the TechSash Organic/Recyclable dataset supplemented with mapped categories from the RealWaste dataset, targeting ≥90% test accuracy.

2. **Design a segregation status classifier** (Phase 2) that evaluates scene-level images of waste collections to determine proper vs. improper segregation.

3. **Develop a Flask REST API** that serves predictions from both models, manages prediction history, and provides model status information.

4. **Create a React frontend** with an intuitive drag-and-drop image upload interface, real-time prediction display with confidence scores, and a history dashboard.

5. **Document the complete methodology** including dataset preparation, model architecture decisions, training procedures, evaluation metrics, and deployment considerations.

6. **Plan Phase 2 extensions** including ward-level analytics, geospatial mapping of segregation compliance, and integration with municipal waste management systems.
