# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## FORGE AI CAM — AI-POWERED FITNESS TRACKING AND WORKOUT ANALYSIS SYSTEM

**Document Version:** 1.0  
**Project:** Forge AI Cam  
**Document Type:** Software Requirements Specification  
**Status:** Proposed / Initial Development  
**Primary Platform:** Web Application  
**Target Users:** Individuals performing home workouts and fitness training  
**Primary AI Technology:** MediaPipe Pose Landmarker  
**Frontend:** React, TypeScript, Vite  
**Backend (planned):** Node.js, Express.js  
**Database (planned):** PostgreSQL with Prisma ORM  

---

# 1. INTRODUCTION

## 1.1 Purpose

The purpose of this document is to define the functional and non-functional requirements of Forge AI Cam, an AI-powered fitness tracking and exercise analysis system.

Forge AI Cam aims to transform a standard webcam into an intelligent fitness assistant capable of tracking a user's body movements, analyzing exercise posture, counting repetitions, identifying potential form errors, and providing real-time feedback during workouts.

Traditional fitness applications primarily depend on manually entered workout information, pre-recorded exercise videos, or wearable devices. Forge AI Cam aims to provide a more interactive experience by using computer vision and pose estimation to analyze the user's movements directly through their camera.

The system will use MediaPipe Pose Landmarker to identify human body landmarks and custom exercise-analysis algorithms to interpret those landmarks. It will evaluate movement patterns, determine exercise phases, count valid repetitions, and provide corrective feedback based on predefined exercise-specific rules.

This document specifies the complete system scope, architecture, user requirements, functional requirements, non-functional requirements, data requirements, interfaces, constraints, and testing criteria.

## 1.2 Project Overview

Forge AI Cam is a computer-vision-based workout assistant designed to help users perform exercises correctly and monitor their workout progress.

The system will combine the following capabilities:

1. Real-time human pose detection and tracking.
2. Body landmark identification and skeletal visualization.
3. Exercise selection and workout configuration.
4. Exercise-specific posture and movement analysis.
5. Automatic repetition counting.
6. Real-time form correction and feedback.
7. Workout timer and set management.
8. Exercise performance scoring.
9. Workout session summaries.
10. Historical workout tracking and analytics.
11. Integration with the larger Forge fitness platform.

The system will primarily process camera frames locally within the browser. Raw camera footage will not need to be transmitted to the backend for normal workout analysis.

## 1.3 Problem Statement

People performing workouts at home often lack access to trainers who can continuously monitor their exercise technique.

Common problems include:

- Incorrect exercise posture.
- Improper joint alignment.
- Incomplete repetitions.
- Incorrect movement range.
- Inconsistent workout tracking.
- Manual repetition counting.
- Difficulty monitoring workout improvement.
- Lack of immediate feedback when an exercise is performed incorrectly.

Existing fitness applications often provide exercise demonstrations and workout plans but do not continuously analyze the user's actual movements.

Forge AI Cam addresses these limitations by introducing a camera-based AI system that tracks body movements and evaluates exercise performance in real time.

## 1.4 Project Objectives

The major objectives are:

- Develop a real-time human pose tracking system using MediaPipe.
- Identify relevant body joints and landmarks.
- Calculate joint angles and movement characteristics.
- Develop exercise-specific algorithms for evaluating movement.
- Automatically count completed repetitions.
- Detect predefined exercise form deviations.
- Provide immediate and understandable corrective feedback.
- Track workout duration, repetitions, sets, and performance.
- Maintain workout history and provide progress visualizations.
- Build a modular architecture that can support additional exercises.
- Integrate the system into the existing Forge fitness ecosystem.

## 1.5 Scope

### In Scope

The initial system will include:

- Webcam access and camera initialization.
- Real-time pose estimation.
- 33-point human pose landmark tracking through MediaPipe.
- Skeleton and landmark visualization.
- Exercise selection.
- Exercise-specific camera positioning instructions.
- Joint-angle calculations.
- Landmark confidence validation.
- Movement smoothing.
- Exercise phase detection.
- Repetition counting.
- Basic form error detection.
- Real-time textual feedback.
- Workout timers.
- Set and repetition tracking.
- Workout session summaries.
- Workout history.
- Performance graphs and statistics.
- Basic user settings.
- Privacy controls.
- Backend integration for storing workout information.

### Out of Scope for Initial Release

The following capabilities may be introduced in future versions:

- Full 3D biomechanical analysis.
- Medical diagnosis or injury prediction.
- Guaranteed injury prevention.
- Automatic recognition of every possible exercise.
- Full-body movement classification across arbitrary activities.
- Multi-person workout tracking.
- Advanced personalized training recommendations.
- Wearable-device synchronization.
- Native Android and iOS applications.
- LLM-based analysis of every camera frame.
- Cloud-based storage of continuous raw video recordings.

## 1.6 Intended Audience

This document is intended for:

- Project developers.
- Frontend developers.
- Backend developers.
- Computer vision and AI developers.
- Software testers.
- Project evaluators.
- Future contributors to Forge.

---

# 2. SYSTEM DESCRIPTION

## 2.1 Product Perspective

Forge AI Cam will initially be developed as an independent web application to allow the pose-tracking and exercise-analysis components to be developed, tested, and evaluated separately.

After validation, it will be integrated into the main Forge fitness platform.

The system will contain three primary layers:

**1. Presentation Layer**

Responsible for the user interface, camera display, skeleton overlay, exercise selection, workout controls, feedback messages, and analytics dashboards.

**2. AI and Exercise Analysis Layer**

Responsible for pose estimation, landmark processing, joint-angle calculations, movement analysis, form evaluation, and repetition counting.

**3. Application and Data Layer**

Responsible for user information, exercise configurations, workout sessions, session summaries, and historical performance data.

## 2.2 Major System Modules

| Module | Description |
|---|---|
| Camera Management | Accesses and manages the user's webcam |
| Pose Estimation | Detects human body landmarks |
| Skeleton Visualization | Displays detected body joints and connections |
| Exercise Library | Maintains supported exercises and their instructions |
| Exercise Analyzer | Evaluates exercise-specific movements |
| Rep Counter | Counts completed repetitions |
| Form Analyzer | Identifies predefined form deviations |
| Feedback Engine | Generates real-time corrective messages |
| Workout Manager | Manages sets, rest periods, and workout duration |
| Session Manager | Creates and stores workout sessions |
| Analytics Dashboard | Displays performance and historical progress |
| User Settings | Stores preferences and configuration |

## 2.3 User Classes

### A. Registered User

A user who can access the workout system, select exercises, perform workouts, and review previous sessions.

### B. Guest User

A user who can access basic camera tracking and workout functionality without creating an account, subject to application configuration.

### C. Administrator

An administrator responsible for managing exercise configurations, supported exercise definitions, and application-level settings, if an administrative interface is implemented.

---

# 3. SYSTEM ARCHITECTURE

## 3.1 Proposed Architecture

The system will follow a modular architecture.

**Camera Input → Pose Estimation → Landmark Processing → Exercise Analysis → Feedback and Rep Counting → Session Tracking → Analytics**

### 3.1.1 Camera Input Module

Responsibilities:

- Request webcam permission.
- Initialize the camera.
- Capture live video frames.
- Display the camera feed.
- Handle camera permission errors.
- Stop camera streams when the workout ends.
- Support camera switching where available.

Technology: Browser MediaDevices API and HTMLVideoElement.

### 3.1.2 Pose Estimation Module

MediaPipe Pose Landmarker will be used for human pose estimation.

It identifies 33 body landmarks, including:

- Nose.
- Left and right shoulders.
- Left and right elbows.
- Left and right wrists.
- Left and right hips.
- Left and right knees.
- Left and right ankles.
- Heels and foot landmarks.

The model provides normalized landmark coordinates and visibility-related confidence information. It can also provide estimated world landmarks.

Each detected landmark can be represented using:

- X coordinate.
- Y coordinate.
- Z coordinate.
- Visibility or presence confidence, where available.

The pose-estimation module will be responsible only for detecting body landmarks. It will not independently determine whether an exercise is being performed correctly.

### 3.1.3 Landmark Processing Module

Raw landmark values may fluctuate between consecutive video frames.

This module will:

- Validate landmark visibility.
- Filter unreliable landmark observations.
- Smooth landmark coordinates.
- Calculate relevant joint angles.
- Track changes in body position.
- Normalize relevant movement measurements.
- Prepare processed data for exercise analysis.

A smoothing technique such as an exponential moving average may be used.

Example:

Smoothed Angle = α × Current Angle + (1 − α) × Previous Smoothed Angle

Here, α controls the amount of smoothing.

### 3.1.4 Exercise Analysis Module

This module interprets body movement based on the selected exercise.

Each exercise will have its own analyzer containing:

- Required landmarks.
- Required camera orientation.
- Joint-angle calculations.
- Movement phases.
- Valid repetition conditions.
- Form-checking rules.
- Feedback messages.

The architecture must allow new exercise analyzers to be added without changing the core pose-estimation module.

### 3.1.5 Repetition Counting Module

The repetition counter will use a finite-state-machine approach.

For example, a push-up may contain the following states:

1. READY / TOP POSITION.
2. DESCENDING.
3. BOTTOM POSITION.
4. ASCENDING.
5. COMPLETED REP.

A repetition should be counted only after a valid movement cycle is completed.

The system must not count a repetition merely because a particular joint angle crosses one threshold.

### 3.1.6 Feedback Engine

The feedback engine will evaluate the results produced by the exercise analyzer.

It will generate feedback such as:

- Keep your back straight.
- Go lower.
- Extend your arms fully.
- Maintain proper knee alignment.
- Move more slowly.
- Keep your elbows close to your body.

Feedback should be generated from deterministic exercise-specific rules.

An LLM should not be called for every video frame. This would introduce unnecessary latency and cost. An LLM may be considered later for session summaries or conversational fitness guidance.

---

# 4. FUNCTIONAL REQUIREMENTS

Each functional requirement is assigned a unique identifier and priority.

Priority definitions:

- **P0 – Critical:** Required for the core system to operate.
- **P1 – High:** Required for a usable first complete release.
- **P2 – Medium:** Important enhancement.
- **P3 – Future:** Optional or advanced functionality.

## 4.1 User and Application Management

**FR-001: User Access**

The system shall allow users to access the AI Cam interface.

Priority: P1.

**FR-002: User Authentication**

The system shall support user authentication when integrated with the main Forge platform.

Priority: P1.

**FR-003: User Profile**

The system shall maintain basic user information and workout preferences where required.

Priority: P2.

**FR-004: Guest Access**

The system may allow users to try basic camera-based workout tracking without registering.

Priority: P2.

## 4.2 Camera Management

**FR-005: Camera Permission**

The system shall request permission before accessing the user's webcam.

**FR-006: Camera Initialization**

The system shall initialize the webcam and display the live video feed.

**FR-007: Camera Error Handling**

The system shall display meaningful messages when:

- Camera permission is denied.
- No camera is detected.
- The camera is being used by another application.
- The camera stream cannot be initialized.
- The camera is disconnected during a workout.

**FR-008: Camera Shutdown**

The system shall stop active media tracks when the user exits the workout or closes the camera interface.

**FR-009: Camera Selection**

The system should allow the user to select an available camera where multiple devices are present.

Priority: P2.

**FR-010: Camera Position Guidance**

The system shall display instructions describing the recommended camera position for the selected exercise.

For example:

- Push-ups: side view.
- Squats: side view or suitable front-oblique view, depending on the rule being evaluated.
- Bicep curls: front view.
- Planks: side view.

**FR-011: Camera Readiness Validation**

Before starting an exercise, the system should validate that the required body landmarks are sufficiently visible.

The system should display a warning if the user is outside the frame or important joints are obscured.

Priority: P1.

## 4.3 Pose Detection and Body Tracking

**FR-012: Pose Model Initialization**

The system shall initialize the MediaPipe Pose Landmarker model before processing live camera frames.

**FR-013: Landmark Detection**

The system shall detect available human body landmarks in each processed frame.

**FR-014: Real-Time Pose Tracking**

The system shall continuously process video frames and update the detected pose.

**FR-015: Skeleton Rendering**

The system shall draw a visual skeleton by connecting relevant body landmarks.

**FR-016: Landmark Confidence**

The system shall evaluate landmark visibility or confidence before using a landmark for important calculations.

**FR-017: Pose Loss Detection**

The system shall identify when the user's pose is no longer reliably detected.

**FR-018: Multiple Pose Handling**

The initial version shall analyze one user at a time.

Additional multi-person tracking may be considered in a future release.

**FR-019: Landmark Smoothing**

The system shall smooth noisy landmark positions or calculated angles to reduce unstable feedback.

**FR-020: Pose Processing Status**

The interface should indicate whether pose tracking is active, loading, unavailable, or experiencing tracking problems.

## 4.4 Exercise Library and Selection

**FR-021: Exercise Library**

The system shall provide a list of supported exercises.

**FR-022: Exercise Categories**

Exercises shall be grouped into relevant categories, such as:

- Chest.
- Back.
- Shoulders.
- Arms.
- Legs.
- Core.
- Full Body.

**FR-023: Exercise Information**

Each exercise shall contain:

- Exercise name.
- Description.
- Target muscle groups.
- Instructions.
- Recommended camera orientation.
- Required landmarks.
- Supported form checks.
- Rep-counting rules.
- Exercise difficulty, where configured.

**FR-024: Exercise Selection**

The user shall be able to select an exercise before starting a workout.

**FR-025: Exercise Demonstration**

The system should display an instructional animation, GIF, or video demonstrating the selected exercise.

**FR-026: Exercise Configuration**

The system should allow the user to configure:

- Target repetitions.
- Number of sets.
- Rest duration.
- Workout duration, where applicable.

**FR-027: Exercise Extensibility**

The system shall support adding new exercise definitions without rewriting the core camera and pose-estimation modules.

## 4.5 Joint Angle and Movement Analysis

**FR-028: Joint Angle Calculation**

The system shall calculate relevant joint angles using detected landmarks.

Examples:

- Elbow angle.
- Knee angle.
- Hip angle.
- Shoulder angle.

For three points A, B, and C, where B is the joint:

Angle ABC = arccos(((A − B) · (C − B)) / (|A − B| × |C − B|))

The result shall be converted into degrees.

**FR-029: Exercise-Specific Measurements**

The system shall calculate only the measurements needed by the selected exercise analyzer.

**FR-030: Movement Phase Detection**

The system shall identify the movement phase based on joint angles and other relevant landmark relationships.

**FR-031: Movement Range Analysis**

The system should evaluate whether the user achieves the configured movement range.

**FR-032: Movement Stability**

The system should detect excessive movement fluctuations where the selected exercise supports such a check.

**FR-033: Invalid Measurement Handling**

The system shall avoid making exercise decisions when the necessary landmarks are missing or unreliable.

## 4.6 Exercise Form Analysis

**FR-034: Form Evaluation**

The system shall evaluate exercise form using predefined exercise-specific rules.

**FR-035: Form Error Detection**

The system shall identify supported form deviations.

Examples include:

- Incomplete movement range.
- Incorrect joint angle.
- Excessive trunk movement.
- Improper body alignment.
- Incorrect elbow position.
- Uneven movement between sides.

These checks will depend on the exercise and camera view.

**FR-036: Real-Time Feedback**

The system shall provide feedback when a supported form error is detected.

**FR-037: Feedback Prioritization**

The system should prioritize the most important actionable feedback rather than displaying multiple conflicting messages simultaneously.

**FR-038: Feedback Stability**

The system should avoid displaying feedback based on a single unreliable frame. A condition should generally persist across multiple valid frames before being reported.

**FR-039: Feedback Recovery**

The system should indicate when the user has corrected a previously detected form issue.

**FR-040: Exercise-Specific Rules**

Each exercise shall maintain its own form-analysis rules and thresholds.

**FR-041: Form Evaluation Confidence**

The system should distinguish between:

- Correctly observed movement.
- Observed form deviation.
- Insufficient visual evidence.

The system must not label an exercise as incorrect when required landmarks are not visible.

## 4.7 Repetition Counting

**FR-042: Automatic Repetition Counting**

The system shall automatically count valid repetitions for supported exercises.

**FR-043: State-Based Counting**

The system shall use an exercise-specific movement state machine or equivalent movement-cycle logic.

**FR-044: Complete Movement Validation**

A repetition shall be counted only after the required movement phases are completed.

**FR-045: Invalid Rep Prevention**

The system shall avoid counting:

- Partial movements that do not satisfy configured criteria.
- Repeated frames in the same movement phase.
- Incomplete movement cycles.
- Noisy angle fluctuations around a threshold.

**FR-046: Live Counter**

The interface shall display the current repetition count.

**FR-047: Counter Reset**

The system shall reset the repetition count when a new set or exercise begins, according to the session configuration.

**FR-048: Manual Correction**

The user should be able to correct a repetition count if the system makes a mistake.

Priority: P2.

**FR-049: Target Rep Tracking**

The system shall display progress against the user's target repetitions.

**FR-050: Rep Event Recording**

The system should record the timestamp and relevant analysis information associated with each completed repetition.

Priority: P2.

## 4.8 Workout and Set Management

**FR-051: Start Workout**

The user shall be able to start a selected exercise session after the camera and pose tracker are ready.

**FR-052: Pause Workout**

The user shall be able to pause the workout.

**FR-053: Resume Workout**

The user shall be able to resume a paused workout.

**FR-054: End Workout**

The user shall be able to end the workout.

**FR-055: Set Management**

The system shall support multiple sets for an exercise.

**FR-056: Rest Timer**

The system should provide a rest timer between sets.

**FR-057: Workout Timer**

The system shall track the workout duration.

**FR-058: Set Completion**

The system shall identify when the configured target repetitions for a set have been reached.

**FR-059: Exercise Completion**

The system shall allow users to finish an exercise and move to another exercise in the workout.

**FR-060: Interrupted Workout**

The system should handle interrupted sessions and clearly distinguish completed, paused, and abandoned workouts.

## 4.9 Performance Scoring

**FR-061: Exercise Performance Score**

The system may calculate an exercise performance score based on measurable exercise-specific criteria.

**FR-062: Form Consistency**

The system should calculate the proportion of analyzed repetitions that satisfied the configured form checks.

**FR-063: Movement Range Metrics**

The system may record movement-range measurements for supported exercises.

**FR-064: Score Transparency**

The system shall provide an explanation of what contributes to a performance score.

A score must not be represented as a medical assessment or guaranteed measure of injury risk.

## 4.10 Workout Summary and Analytics

**FR-065: Session Summary**

At the end of a workout, the system shall display a session summary.

The summary may contain:

- Exercise name.
- Total repetitions.
- Completed sets.
- Workout duration.
- Average time per repetition.
- Valid and flagged repetitions, where supported.
- Form consistency.
- Exercise performance score, where implemented.

**FR-066: Workout History**

The system shall store and display previous workout sessions for authenticated users.

**FR-067: Historical Performance**

The system should allow users to compare workout performance across different dates.

**FR-068: Progress Charts**

The system shall support graphical representation of workout data.

Examples:

- Repetitions over time.
- Workout duration over time.
- Total completed sets.
- Exercise frequency.
- Form consistency over time.

**FR-069: Exercise-Based Filtering**

Users should be able to filter workout history by exercise and date range.

**FR-070: Personal Records**

The system may identify personal records, such as the highest completed repetition count or longest plank duration, where the metric is meaningful.

---

# 5. SUPPORTED EXERCISES AND EXERCISE-SPECIFIC REQUIREMENTS

The exercise-analysis engine must be modular. Each supported exercise will have an independent analyzer.

The following exercises form the proposed initial exercise library.

## 5.1 Push-Ups

**Target Muscles:** Chest, triceps, shoulders, core.

**Recommended Camera View:** Side view.

**Important Landmarks:**

- Left and right shoulders.
- Left and right elbows.
- Left and right wrists.
- Left and right hips.
- Left and right ankles.

**Important Measurements:**

- Elbow angle.
- Shoulder, hip, and ankle alignment.
- Body position throughout the movement.

**Movement States:**

1. Top position.
2. Descending.
3. Bottom position.
4. Ascending.
5. Rep completion.

**Rep Counting Logic:**

A repetition should be counted after the user moves from a valid top position through the required bottom position and returns to a valid top position.

**Potential Form Checks:**

- Incomplete descent.
- Incomplete arm extension.
- Excessive hip sag.
- Excessive hip elevation.
- Poor body alignment.

## 5.2 Squats

**Target Muscles:** Quadriceps, glutes, hamstrings.

**Recommended Camera View:** Side view for depth and trunk-position checks; front or oblique view for supported knee-alignment checks.

**Important Landmarks:**

- Shoulders.
- Hips.
- Knees.
- Ankles.

**Important Measurements:**

- Knee angle.
- Hip angle.
- Trunk inclination.
- Hip movement relative to the knees.

**Movement States:**

1. Standing.
2. Descending.
3. Bottom position.
4. Ascending.
5. Standing completion.

**Potential Form Checks:**

- Insufficient squat depth.
- Incomplete return to standing.
- Excessive trunk inclination, where measurable.
- Knee alignment deviation, when the camera view supports it.

## 5.3 Bicep Curls

**Target Muscles:** Biceps and forearms.

**Recommended Camera View:** Front or slight oblique view.

**Important Landmarks:**

- Shoulders.
- Elbows.
- Wrists.
- Hips.

**Important Measurements:**

- Elbow angle.
- Upper-arm movement.
- Wrist position.
- Shoulder movement.

**Movement States:**

1. Extended position.
2. Curling upward.
3. Contracted position.
4. Lowering.
5. Rep completion.

**Potential Form Checks:**

- Incomplete curl.
- Incomplete arm extension.
- Excessive shoulder movement.
- Excessive upper-body swinging.

## 5.4 Plank

**Target Muscles:** Core, shoulders, glutes.

**Recommended Camera View:** Side view.

**Important Landmarks:**

- Shoulders.
- Hips.
- Ankles.
- Elbows.

**Measurements:**

- Shoulder-hip-ankle alignment.
- Trunk angle.
- Pose stability over time.

**Analysis:**

Plank is a timed static exercise, so it should not use conventional repetition counting.

The system shall:

- Detect the plank position.
- Validate required landmark visibility.
- Start the timer when the position satisfies configured conditions.
- Detect sustained deviations.
- Pause or flag the timer when the pose is no longer valid, according to the configured rules.
- Record total valid hold duration.

## 5.5 Exercise Expansion

Future exercises may include:

- Lunges.
- Shoulder presses.
- Lateral raises.
- Jumping jacks.
- Mountain climbers.
- Glute bridges.
- Calf raises.
- Side planks.

Each new exercise must define its camera orientation, required landmarks, measurements, movement states, repetition rules, and form checks before being marked as supported.

---

# 6. EXERCISE ANALYSIS ENGINE

## 6.1 Overview

The exercise-analysis engine is the core logic responsible for interpreting detected human movement.

MediaPipe supplies body landmark coordinates. The analysis engine uses those coordinates to determine how the user is moving.

The engine must be independent of the user interface and should expose a consistent interface to the frontend.

## 6.2 Proposed Exercise Analyzer Interface

Each exercise analyzer should conceptually provide:

- Initialization.
- Landmark validation.
- Measurement calculation.
- Movement-state update.
- Repetition detection.
- Form evaluation.
- Feedback generation.
- Session reset.

An exercise analyzer must not directly access the webcam or render UI elements.

## 6.3 Joint Angle Calculation

The system shall calculate the angle between three detected landmarks.

For example, the elbow angle uses:

- Shoulder as point A.
- Elbow as point B.
- Wrist as point C.

The angle is calculated at point B.

The calculation must handle zero-length vectors and invalid landmark coordinates to prevent numerical errors.

## 6.4 Movement State Machine

A finite-state machine shall be used to track exercise progression.

Example: Push-up.

| Current State | Condition | Next State |
|---|---|---|
| READY | User begins lowering | DESCENDING |
| DESCENDING | Required bottom position reached | BOTTOM |
| BOTTOM | User begins pushing upward | ASCENDING |
| ASCENDING | Valid top position reached | READY |
| READY | Complete cycle confirmed | Rep count increases |

The implementation should use separate entry and exit thresholds, where appropriate, to prevent rapid state changes caused by small landmark fluctuations.

This is known as hysteresis.

## 6.5 Rep Counting Reliability

The repetition counter must:

- Validate the starting position.
- Validate the bottom or peak position.
- Validate the return position.
- Prevent duplicate counts.
- Handle temporary tracking loss.
- Avoid counting during paused sessions.
- Avoid counting movements that do not satisfy the exercise definition.

A configurable debounce or minimum phase duration may be used to reject noisy transitions.

## 6.6 Form Evaluation Rules

Form evaluation must be based on measurable conditions.

Example:

| Exercise | Condition | Feedback |
|---|---|---|
| Push-up | Insufficient elbow flexion | Go lower |
| Push-up | Excessive hip sag | Keep your body aligned |
| Squat | Insufficient configured depth | Try going a little lower |
| Bicep curl | Excessive shoulder movement | Keep your elbows stable |
| Plank | Sustained body alignment deviation | Adjust your body alignment |

These are examples of possible rules, not universal biomechanical thresholds. Thresholds must be calibrated and validated for the selected camera view and exercise.

## 6.7 Feedback Prioritization

The system should:

1. Validate required landmarks.
2. Evaluate the exercise state.
3. Evaluate active form rules.
4. Prioritize the most actionable issue.
5. Display feedback only when the condition is sufficiently stable.
6. Remove or update the feedback when the condition changes.

If tracking confidence is inadequate, the system should request repositioning instead of providing potentially misleading form feedback.

---

# 7. USER INTERFACE REQUIREMENTS

## 7.1 Main AI Cam Dashboard

The main dashboard should display:

- Available exercises.
- Exercise categories.
- Exercise descriptions.
- Start workout action.
- Previous session summary.
- Workout statistics.

## 7.2 Workout Setup Screen

Before starting a workout, the user should be able to:

- Select an exercise.
- Set target repetitions.
- Set the number of sets.
- Configure rest duration.
- View exercise instructions.
- View the recommended camera position.

## 7.3 Live Workout Screen

The live workout screen is the primary interface.

It should contain:

**Camera Area**
- Live camera feed.
- Skeleton overlay.
- Landmark visualization.
- Tracking status.
- Camera positioning guidance.

**Workout Information**
- Selected exercise.
- Current set.
- Current repetitions.
- Target repetitions.
- Workout timer.
- Set progress.

**AI Feedback**
- Current form status.
- Corrective feedback.
- Tracking warnings.
- Rep completion indication.

**Workout Controls**
- Start.
- Pause.
- Resume.
- Finish workout.
- Reset, where supported.

The camera and feedback must remain visually clear and should not obscure important body landmarks.

## 7.4 Workout Completion Screen

The completion screen should display:

- Exercise name.
- Total sets.
- Total repetitions.
- Total duration.
- Form statistics, if available.
- Performance score, if implemented.
- Session completion status.

The user should be able to save the session and return to the dashboard.

## 7.5 Analytics Dashboard

The analytics dashboard should provide:

- Total workouts.
- Total repetitions.
- Total workout time.
- Exercise-wise history.
- Weekly activity.
- Progress charts.
- Personal records.
- Form consistency trends.

Charts must use saved session data and must not imply that a trend is statistically meaningful when there is insufficient data.

---

# 8. NON-FUNCTIONAL REQUIREMENTS

## 8.1 Performance

**NFR-001: Real-Time Processing**

The system should process camera frames continuously with sufficient responsiveness for real-time workout feedback.

The target performance should be measured on defined reference hardware rather than assumed to be identical across all devices.

**NFR-002: Frame Rate**

The initial performance target should be approximately 20–30 processed frames per second on supported desktop hardware.

Lower processing rates should degrade gracefully rather than breaking the workout.

**NFR-003: Feedback Latency**

The target for visible feedback after a sufficiently persistent form condition is detected should be less than 500 milliseconds on reference hardware.

This target excludes the time required for the user to physically perform the movement.

**NFR-004: UI Responsiveness**

Pose processing must not make the application interface unresponsive.

If synchronous processing causes performance problems, processing should be moved to a Web Worker or otherwise isolated.

## 8.2 Accuracy and Reliability

**NFR-005: Rep Counting Accuracy**

The system should target at least 90% repetition-count agreement against manually annotated test sessions for supported exercises under defined testing conditions.

**NFR-006: Form Detection Accuracy**

Each form rule must be independently evaluated using manually labelled examples.

The project should measure precision, recall, and false-positive rates rather than relying on an overall subjective score.

**NFR-007: Tracking Reliability**

The system should identify insufficient landmark visibility and avoid producing unreliable exercise judgments.

**NFR-008: Session Reliability**

The system should handle camera interruptions, temporary tracking loss, and application errors without silently corrupting saved workout data.

## 8.3 Usability

**NFR-009:** The interface should be understandable to users without technical knowledge of computer vision.

**NFR-010:** Exercise instructions should be concise and actionable.

**NFR-011:** Users should be able to start and stop workouts with minimal interaction.

**NFR-012:** Important workout information should remain visible during exercise.

## 8.4 Compatibility

**NFR-013:** The application should support modern browsers that provide the required webcam and WebAssembly capabilities.

**NFR-014:** The system should support desktop and laptop webcams.

**NFR-015:** Mobile browser support may be introduced progressively and should be validated separately.

## 8.5 Security

**NFR-016:** Camera access must require browser permission.

**NFR-017:** Backend endpoints must validate authenticated user identity.

**NFR-018:** Users must not be able to access another user's private workout history.

**NFR-019:** Sensitive user information must not be exposed in client-side logs or API responses.

**NFR-020:** API communication should use HTTPS in production.

## 8.6 Privacy

**NFR-021:** Camera processing should occur locally in the browser by default.

**NFR-022:** Raw camera footage should not be uploaded or stored unless a separate, explicit feature and consent process is implemented.

**NFR-023:** The camera stream must be stopped when the user ends the session or leaves the camera interface.

**NFR-024:** The system should clearly communicate when the camera is active.

## 8.7 Maintainability

**NFR-025:** Pose estimation, landmark processing, exercise analysis, feedback, and session management should be separate modules.

**NFR-026:** New exercises should be implementable through exercise-specific analyzers.

**NFR-027:** Exercise thresholds should be configurable instead of being scattered throughout the codebase.

**NFR-028:** Important exercise-analysis logic should have automated unit tests.

---

# 9. TECHNOLOGY STACK

The following stack is proposed for the initial implementation.

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React | User interface |
| Language | TypeScript | Type-safe application logic |
| Build Tool | Vite | Development and build |
| Styling | CSS / Tailwind CSS | Interface design |
| Pose Estimation | MediaPipe Pose Landmarker | Human pose detection |
| Camera | MediaDevices API | Webcam access |
| Rendering | HTML Canvas | Skeleton visualization |
| Exercise Logic | TypeScript | Joint angles, form checks, rep counting |
| Backend | Node.js + Express.js | Application APIs |
| Database | PostgreSQL | Persistent application data |
| ORM | Prisma | Database access |
| Charts | Recharts | Workout analytics |
| Authentication | Existing Forge authentication | User access |
| Version Control | Git + GitHub | Source management |

The AI Cam prototype should first operate independently of the backend wherever possible. Camera access, pose estimation, skeleton rendering, and basic exercise analysis should be validated before persistent session storage is introduced.

---

# 10. SYSTEM DATA REQUIREMENTS

## 10.1 User Entity

Suggested fields:

- user_id
- name
- email
- created_at
- updated_at

Authentication credentials should be handled by the existing authentication system and should not be duplicated unnecessarily.

## 10.2 Exercise Entity

Suggested fields:

- exercise_id
- exercise_name
- category
- description
- target_muscles
- difficulty
- camera_view
- instructions
- is_active

## 10.3 Exercise Configuration

This entity or configuration structure defines how the system analyzes an exercise.

Suggested fields:

- configuration_id
- exercise_id
- required_landmarks
- relevant_joint_angles
- movement_states
- angle_thresholds
- form_rules
- feedback_messages
- configuration_version

Exercise configuration should support versioning so that historical workout results can be interpreted in the context of the rules used at that time.

## 10.4 Workout Session Entity

Suggested fields:

- session_id
- user_id
- start_time
- end_time
- duration_seconds
- session_status
- total_exercises
- created_at

## 10.5 Workout Exercise Entity

Suggested fields:

- workout_exercise_id
- session_id
- exercise_id
- set_count
- total_repetitions
- target_repetitions
- exercise_duration
- completion_status

## 10.6 Workout Set Entity

Suggested fields:

- set_id
- workout_exercise_id
- set_number
- completed_repetitions
- target_repetitions
- duration_seconds
- rest_duration_seconds
- set_status

## 10.7 Rep Event Entity

Optional detailed event storage.

Suggested fields:

- rep_event_id
- set_id
- repetition_number
- timestamp
- movement_duration
- form_status
- measured_metrics

This data can be used for advanced analysis, but storing every camera frame or every landmark observation is not required for the initial release.

## 10.8 Form Feedback Entity

Suggested fields:

- feedback_id
- set_id
- rule_id
- feedback_message
- severity
- timestamp
- duration_ms

The application should avoid excessive event storage. It may aggregate repeated feedback events into session-level statistics.

## 10.9 Relationships

- One user can have multiple workout sessions.
- One workout session can contain multiple exercises.
- One exercise can appear in multiple workout sessions.
- One workout exercise can contain multiple sets.
- One set can contain multiple repetition events.
- One set can generate multiple form-feedback events.
- One exercise can have multiple configuration versions.

---

# 11. API REQUIREMENTS

The backend will manage persistent application data. Real-time pose estimation and exercise analysis should remain in the frontend initially.

Proposed REST endpoints:

## 11.1 Exercise APIs

**GET /api/exercises**

Returns the supported exercise library.

**GET /api/exercises/:id**

Returns the details of a specific exercise.

## 11.2 Workout Session APIs

**POST /api/workouts/sessions**

Creates a workout session.

**GET /api/workouts/sessions**

Returns the authenticated user's workout history.

**GET /api/workouts/sessions/:id**

Returns details of a specific workout session.

**PATCH /api/workouts/sessions/:id**

Updates session status or other permitted session information.

**POST /api/workouts/sessions/:id/complete**

Marks a session as completed and stores its final summary.

## 11.3 Workout Set APIs

**POST /api/workouts/sessions/:id/exercises**

Adds an exercise to a session.

**POST /api/workouts/sets**

Creates a set record.

**PATCH /api/workouts/sets/:id**

Updates repetitions, duration, and set status.

## 11.4 Analytics APIs

**GET /api/analytics/overview**

Returns general workout statistics.

**GET /api/analytics/exercises/:id**

Returns exercise-specific progress.

**GET /api/analytics/history**

Returns historical performance data for the requested date range.

All user-specific APIs must enforce authentication and authorization.

---

# 12. USER WORKFLOW

## 12.1 Standard Workout Workflow

1. The user opens Forge AI Cam.
2. The system displays available exercises.
3. The user selects an exercise.
4. The system displays instructions and camera positioning guidance.
5. The user grants camera permission.
6. The system initializes MediaPipe Pose Landmarker.
7. The camera displays the live video feed.
8. The system detects the user's body landmarks.
9. The system validates the required landmarks.
10. The system displays the skeletal overlay.
11. The user adjusts their position if necessary.
12. The user starts the workout.
13. The exercise analyzer processes the user's movement.
14. The rep counter tracks completed repetitions.
15. The feedback engine identifies supported form deviations.
16. The interface displays live repetitions and feedback.
17. The user completes the set.
18. The system starts the configured rest timer.
19. The user completes the remaining sets.
20. The user finishes the exercise.
21. The system calculates the session summary.
22. The session is saved.
23. The user can view workout analytics and history.

## 12.2 Exception Workflows

**Camera Permission Denied**

The system displays an explanation and instructions for enabling camera access.

**User Not Detected**

The system displays a message asking the user to move into the camera frame.

**Required Joint Not Visible**

The system displays a camera-position warning and temporarily suspends unreliable exercise analysis.

**Pose Tracking Lost During Exercise**

The system should avoid counting a repetition based on incomplete movement data. It should recover tracking when the user becomes visible again.

**Application Interrupted**

The system should preserve the last safely saved session state where possible and identify the session as interrupted if it cannot be completed.

---

# 13. ERROR HANDLING

The system shall handle the following error conditions:

| Error | Expected System Behaviour |
|---|---|
| Camera permission denied | Display permission instructions |
| Camera unavailable | Display camera error |
| MediaPipe initialization failure | Display model initialization error |
| GPU delegate unavailable | Attempt supported fallback, such as CPU |
| No person detected | Display positioning guidance |
| Low landmark visibility | Suspend affected analysis |
| Invalid joint angle | Skip the affected measurement |
| Tracking lost | Pause or flag analysis |
| Backend unavailable | Preserve recoverable local session data |
| Session save failure | Inform the user and offer retry |
| Invalid API response | Handle safely without crashing |
| Browser performance degradation | Reduce processing workload where possible |

The system must not silently report a successful repetition when the movement cannot be reliably evaluated.

---

# 14. TESTING REQUIREMENTS

## 14.1 Unit Testing

Individual modules must be tested independently.

Examples:

- Joint-angle calculation.
- Landmark validation.
- Landmark smoothing.
- Rep-counting state transitions.
- Form-rule evaluation.
- Workout timer.
- Set completion.
- Session-summary calculation.

## 14.2 Integration Testing

The following integrations must be tested:

- Webcam to video element.
- Video frames to MediaPipe.
- MediaPipe output to landmark processor.
- Landmark processor to exercise analyzer.
- Exercise analyzer to rep counter.
- Exercise analyzer to feedback engine.
- Workout manager to backend APIs.
- Session storage to analytics dashboard.

## 14.3 Functional Testing

Test cases should include:

- Successful camera initialization.
- Camera permission denial.
- Exercise selection.
- Correct pose detection.
- Skeleton overlay rendering.
- Correct repetition counting.
- Prevention of duplicate repetitions.
- Form feedback generation.
- Workout pause and resume.
- Set completion.
- Workout summary generation.
- Historical session retrieval.

## 14.4 Accuracy Testing

Each supported exercise should be evaluated using manually annotated workout recordings or controlled live test sessions.

For repetition counting:

Rep Count Accuracy = (Correctly Counted Repetitions / Actual Repetitions) × 100

For form detection, measure:

- Precision.
- Recall.
- F1-score.
- False-positive rate.
- False-negative rate.

Testing should include different:

- Body proportions.
- Camera distances.
- Lighting conditions.
- Clothing types.
- Background environments.
- Movement speeds.
- Camera angles.

The system should document which conditions are supported and which are known limitations.

## 14.5 Performance Testing

Measure:

- Average processed FPS.
- Average pose-estimation latency.
- Exercise-analysis latency.
- End-to-end feedback latency.
- CPU usage.
- Memory consumption.
- Camera initialization time.

Testing should be performed on representative low-, mid-, and high-performance devices.

## 14.6 Acceptance Criteria

The initial release will be considered acceptable when:

1. The webcam can be initialized successfully on supported browsers.
2. MediaPipe can detect the user's pose.
3. The skeleton overlay follows the detected body landmarks.
4. The system validates required landmarks before analysis.
5. At least three initial dynamic exercises have working exercise analyzers.
6. A plank timer works as a static exercise mode.
7. Repetition counting operates through complete movement cycles.
8. At least one useful form check is implemented and tested for each supported exercise.
9. The user can start, pause, resume, and end a workout.
10. A completed session produces a valid summary.
11. Workout history can be stored and retrieved.
12. The application handles camera and tracking failures without crashing.

The target accuracy metrics must be evaluated against a documented test dataset before claiming that they have been achieved.

---

# 15. SECURITY, PRIVACY AND ETHICAL CONSIDERATIONS

## 15.1 Camera Privacy

The application must explicitly request permission to access the camera.

Camera processing should happen locally within the browser by default.

The system must not secretly record, transmit, or store camera footage.

## 15.2 Data Privacy

Only necessary workout information should be stored.

Examples include:

- Exercise name.
- Repetition count.
- Set information.
- Workout duration.
- Aggregated form statistics.

Raw video footage is not required for ordinary workout tracking.

## 15.3 Fitness and Medical Disclaimer

Forge AI Cam is a fitness assistance system, not a medical device.

Its feedback is based on visible landmarks and predefined movement rules. It cannot guarantee that an exercise is safe or that a user's technique is medically correct.

The system should encourage users to stop if they experience pain or discomfort and seek qualified professional guidance when needed.

## 15.4 Responsible AI

The system should:

- Communicate uncertainty when tracking is unreliable.
- Avoid presenting unvalidated judgments as facts.
- Avoid misleading performance scores.
- Avoid making medical or injury-risk predictions.
- Be transparent about the limitations of camera-based pose estimation.

---

# 16. TECHNICAL CONSTRAINTS AND ASSUMPTIONS

## 16.1 Constraints

1. Pose estimation quality depends on camera placement, lighting, and visibility.
2. MediaPipe landmarks may fluctuate due to occlusion and rapid movement.
3. A single camera cannot reliably observe every movement dimension.
4. Exercise-specific rules must be implemented and calibrated separately.
5. Browser performance depends on the user's hardware.
6. GPU acceleration may not be available on every device.
7. The initial system will support one user at a time.
8. Some form checks will require specific camera orientations.
9. Repetition counting and form evaluation will not be equally reliable for all exercises.

## 16.2 Assumptions

1. The user has a working webcam.
2. The user grants camera permission.
3. The user has a supported modern browser.
4. The user performs exercises within the camera frame.
5. The environment has sufficient lighting.
6. The initial exercise library is predefined.
7. The user follows the camera-positioning instructions.
8. The backend is available when persistent cloud session storage is required.

---

# 17. DEVELOPMENT ROADMAP

The project should be developed incrementally.

## Phase 1: Camera and Pose Tracking Foundation

- Set up React + TypeScript + Vite.
- Install MediaPipe Tasks Vision.
- Initialize Pose Landmarker.
- Access webcam.
- Detect body landmarks.
- Render skeleton overlay.
- Handle camera and model errors.

**Deliverable:** A working live pose-tracking interface.

## Phase 2: Landmark Processing and Joint Angles

- Create landmark utilities.
- Validate landmark confidence.
- Implement angle calculations.
- Implement smoothing.
- Display selected joint angles.
- Test different camera positions.

**Deliverable:** Reliable joint-angle measurements from live pose data.

## Phase 3: Exercise Analysis Engine

- Create a common exercise analyzer interface.
- Implement movement-state logic.
- Build push-up analyzer.
- Build squat analyzer.
- Build bicep curl analyzer.
- Implement plank timer logic.

**Deliverable:** Exercise-specific movement analysis.

## Phase 4: Rep Counter and Form Feedback

- Implement finite-state repetition counting.
- Prevent duplicate and invalid counts.
- Implement exercise-specific form checks.
- Add feedback prioritization.
- Add live rep counter.
- Add form status display.

**Deliverable:** Live exercise tracking and corrective feedback.

## Phase 5: Workout Management

- Add exercise selection.
- Add target repetitions.
- Add sets.
- Add rest timer.
- Add workout pause and resume.
- Add workout completion flow.

**Deliverable:** A complete interactive workout experience.

## Phase 6: Backend and Database Integration

- Design database models.
- Implement workout session APIs.
- Implement set and exercise APIs.
- Save completed workout summaries.
- Retrieve workout history.
- Integrate user authentication.

**Deliverable:** Persistent workout tracking.

## Phase 7: Analytics and Performance Dashboard

- Implement workout statistics.
- Add exercise-wise progress charts.
- Add repetition history.
- Add duration trends.
- Add form consistency metrics.
- Add personal records.

**Deliverable:** Workout history and analytics dashboard.

## Phase 8: Forge Platform Integration

- Integrate the AI Cam module into Forge.
- Reuse the existing authentication system.
- Reuse the existing user profile.
- Connect workout history to the main dashboard.
- Ensure consistent design and navigation.
- Validate the complete platform workflow.

**Deliverable:** AI Cam integrated into the Forge fitness platform.

---

# 18. PROPOSED PROJECT DIRECTORY STRUCTURE

The initial standalone React + TypeScript application should use a modular structure.

```text
forge-ai-cam/
│
├── public/
│   └── models/
│
├── src/
│   ├── components/
│   │   ├── CameraView.tsx
│   │   ├── SkeletonOverlay.tsx
│   │   ├── RepCounter.tsx
│   │   ├── FeedbackPanel.tsx
│   │   ├── ExerciseSelector.tsx
│   │   ├── WorkoutControls.tsx
│   │   └── WorkoutSummary.tsx
│   │
│   ├── pose/
│   │   ├── poseLandmarker.ts
│   │   ├── landmarkUtils.ts
│   │   ├── angleCalculator.ts
│   │   ├── landmarkSmoother.ts
│   │   └── poseTypes.ts
│   │
│   ├── exercises/
│   │   ├── exerciseTypes.ts
│   │   ├── exerciseRegistry.ts
│   │   ├── pushup/
│   │   │   ├── pushupAnalyzer.ts
│   │   │   └── pushupRules.ts
│   │   ├── squat/
│   │   │   ├── squatAnalyzer.ts
│   │   │   └── squatRules.ts
│   │   ├── bicepCurl/
│   │   │   ├── bicepCurlAnalyzer.ts
│   │   │   └── bicepCurlRules.ts
│   │   └── plank/
│   │       ├── plankAnalyzer.ts
│   │       └── plankRules.ts
│   │
│   ├── workout/
│   │   ├── workoutManager.ts
│   │   ├── repCounter.ts
│   │   ├── setManager.ts
│   │   └── workoutTimer.ts
│   │
│   ├── feedback/
│   │   ├── feedbackEngine.ts
│   │   └── feedbackTypes.ts
│   │
│   ├── services/
│   │   └── workoutApi.ts
│   │
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── LiveWorkout.tsx
│   │   ├── WorkoutHistory.tsx
│   │   └── Analytics.tsx
│   │
│   ├── types/
│   │   └── index.ts
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── package.json
└── README.md
```

The backend can later be organized as a separate service or within the existing Forge backend.

---

# 19. FUTURE ENHANCEMENTS

Potential future capabilities include:

### 19.1 Advanced Pose Analysis

- More sophisticated temporal movement analysis.
- Improved landmark smoothing.
- Better handling of occlusion.
- Exercise-specific 3D landmark analysis.

### 19.2 Personalized Workout Intelligence

- Adaptive repetition targets.
- Exercise recommendations based on workout history.
- Personalized progression plans.
- Training consistency analysis.

### 19.3 AI Workout Coach

A conversational fitness assistant could explain session performance, answer exercise-related questions, and summarize progress using saved workout data.

### 19.4 Voice Feedback

The system could provide spoken instructions such as:

- Rep completed.
- Keep your back straight.
- Three repetitions remaining.
- Rest for 30 seconds.

### 19.5 Advanced Performance Analytics

- Rep tempo analysis.
- Set-to-set performance comparison.
- Movement consistency.
- Exercise-specific range-of-motion trends.
- Long-term training progress.

### 19.6 Expanded Exercise Recognition

The system could eventually investigate automatic exercise classification, allowing it to identify supported movements without requiring the user to select an exercise first.

This should be developed as a separate capability from exercise-specific form analysis.

---

# 20. SUCCESS METRICS

The project should be evaluated using measurable criteria.

| Metric | Proposed Evaluation |
|---|---|
| Pose Detection | Percentage of usable frames with required landmarks detected |
| Rep Counting | Agreement with manually annotated repetitions |
| Form Detection | Precision, recall, and F1-score for each form rule |
| Processing Performance | Average processed FPS |
| Feedback Latency | Time from persistent condition detection to displayed feedback |
| Session Reliability | Percentage of sessions saved without data loss |
| Exercise Coverage | Number of supported exercises |
| User Experience | Usability feedback and task completion rate |

Initial engineering targets:

- At least 90% rep-count agreement on controlled test sessions for supported exercises.
- Approximately 20–30 processed FPS on reference desktop hardware.
- Less than 500 ms feedback latency on reference hardware for stable, detectable conditions.
- Successful session persistence and retrieval.
- No critical camera-resource leaks after ending a session.

These are development targets, not claims of already achieved performance. They must be validated under documented conditions.

---

# 21. CONCLUSION

Forge AI Cam aims to provide a computer-vision-powered fitness experience that goes beyond conventional exercise tracking.

By combining MediaPipe Pose Landmarker, landmark processing, joint-angle calculations, exercise-specific state machines, deterministic form-analysis rules, and workout analytics, the system will be capable of tracking user movements and providing immediate feedback during supported exercises.

The most important architectural decision is to keep pose estimation separate from exercise interpretation.

MediaPipe will identify body landmarks, while the custom exercise-analysis engine will determine movement phases, count repetitions, and evaluate predefined form conditions.

The system will initially support a limited set of exercises with validated movement rules. Its modular design will allow additional exercises, advanced analytics, voice guidance, and personalized workout intelligence to be introduced progressively.

The ultimate goal is to integrate Forge AI Cam into the larger Forge platform as an intelligent fitness assistant that helps users perform workouts, monitor their technique, track their progress, and build consistency.

**END OF SOFTWARE REQUIREMENTS SPECIFICATION**