---
title: Digit Recognition
emoji: ✏️
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Digit recognition app

An web app created using flask and a deep CNN model to identify hand-drawn digits. You can find the model at CNN folder. 

Deployed the app in heroku at <a href="https://digit-recognition-app.herokuapp.com" target=_blank>https://digit-recognition-app.herokuapp.com</a> (P.S. sometimes, the link takes a while to load). Currently, it is only supported on PCs and laptops.


<img width="1303" alt="Screen Shot 2021-03-17 at 10 32 40 PM" src="https://user-images.githubusercontent.com/46661726/111564799-435bd980-8792-11eb-9de2-be6dcdcc5626.png">

---

### Update (2026)

This was my first ML project, originally deployed on Heroku back in 2021. Heroku has
since retired its free tier, so the old link no longer works. I fixed up the outdated
packages (TensorFlow/Keras/NumPy/OpenCV) and redeployed it on Hugging Face Spaces:

**Live demo:** https://huggingface.co/spaces/Sambhav101/digit-recognition
