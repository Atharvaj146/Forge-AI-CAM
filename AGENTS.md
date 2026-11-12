
# Forge AI Cam - Development Rules

## Project Objective
Build a modular, browser-based AI fitness assistant using computer vision.

The application must support:
- Real-time human pose tracking
- Body landmark visualization
- Joint angle calculations
- Exercise-specific movement analysis
- Automatic repetition counting
- Exercise form feedback
- Workout and set management
- Session summaries and analytics

## Technology Stack
- React
- TypeScript
- Vite
- MediaPipe Tasks Vision / Pose Landmarker
- HTML Canvas
- Node.js and Express (when backend is introduced)
- PostgreSQL and Prisma (when database is introduced)
- Recharts (for analytics)

## Architecture Rules
1. Keep camera handling separate from pose estimation.
2. Keep pose estimation separate from landmark processing.
3. Keep landmark processing separate from exercise analysis.
4. Each exercise must have its own analyzer.
5. Keep repetition counting independent from UI components.
6. Keep feedback generation independent from pose detection.
7. Use TypeScript types and interfaces.
8. Avoid unnecessary dependencies and abstractions.

## AI and Computer Vision Rules
1. MediaPipe detects landmarks; it does not determine exercise correctness.
2. Never assume a landmark is reliable without validating its visibility.
3. Handle missing and unreliable landmarks safely.
4. Use smoothing to reduce landmark fluctuations.
5. Calculate joint angles using reusable mathematical utilities.
6. Use state machines for exercise repetition counting.
7. Prevent duplicate and incomplete repetition counts.
8. Make exercise thresholds configurable.
9. Do not use an LLM for frame-by-frame exercise analysis.
10. Do not claim medical accuracy or injury prevention.

## Development Rules
1. Work on one milestone at a time.
2. Inspect existing files before modifying them.
3. Present an implementation plan before significant changes.
4. Explain the purpose of new files and important functions.
5. Do not rewrite working modules unnecessarily.
6. Do not install dependencies without explaining why.
7. Run relevant tests after implementation.
8. Do not claim a feature works without verifying it.
9. Report assumptions, limitations, and known issues.
10. Do not move to the next milestone without approval.

## Code Quality
- Use clear names.
- Avoid giant components.
- Avoid duplicated logic.
- Use reusable utilities.
- Handle errors explicitly.
- Keep functions focused.
- Add comments for non-obvious algorithms.
- Add unit tests for mathematical and exercise-analysis logic.

## Privacy
- Process webcam frames locally by default.
- Do not upload raw video.
- Stop camera tracks when the workout ends.
