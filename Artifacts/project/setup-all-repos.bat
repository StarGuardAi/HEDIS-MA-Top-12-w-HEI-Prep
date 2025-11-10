@echo off
echo Setting up Guardian repo...
cd repo-guardian
git init
git add .
git commit -m "Initial commit: Guardian fraud detection system"
git branch -M main
git remote add origin https://github.com/reichert-sentinel-ai/guardian-fraud-analytics.git
git push -u origin main
cd ..

echo Setting up Foresight repo...
cd repo-foresight
git init
git add .
git commit -m "Initial commit: Foresight crime prediction platform"
git branch -M main
git remote add origin https://github.com/reichert-sentinel-ai/foresight-crime-prediction.git
git push -u origin main
cd ..

echo Setting up Cipher repo...
cd repo-cipher
git init
git add .
git commit -m "Initial commit: Cipher threat tracker"
git branch -M main
git remote add origin https://github.com/reichert-sentinel-ai/cipher-threat-tracker.git
git push -u origin main
cd ..

echo All repos set up and pushed!

