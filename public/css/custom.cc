/* ==============================
   About Page Image Stack
   ============================== */

.about-image-stack {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 2rem auto;
}

.circle-photo {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Layer and offset each image slightly for a "stack" effect */
.offset1 { transform: translateX(-30px) rotate(-3deg); z-index: 4; }
.offset2 { transform: translateX(-50px) rotate(2deg);  z-index: 3; }
.offset3 { transform: translateX(-70px) rotate(-2deg); z-index: 2; }
.offset4 { transform: translateX(-90px) rotate(3deg);  z-index: 1; }

/* Hover animation */
.circle-photo:hover {
  transform: scale(1.1);
  z-index: 10;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}
