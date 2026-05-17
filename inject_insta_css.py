import os

filepath = r"c:\Users\soyst\OneDrive\デスクトップ\vegan\css\inbound.css"

with open(filepath, 'r', encoding='utf-8') as f:
    css = f.read()

insta_css = """
/* =========================================
   Instagram Dynamic Feed Styles
========================================= */
.instagram-feed__grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-top: 24px;
}

@media (min-width: 640px) {
    .instagram-feed__grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }
}

@media (min-width: 1024px) {
    .instagram-feed__grid {
        grid-template-columns: repeat(6, 1fr);
    }
}

.instagram-feed__item {
    position: relative;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    border-radius: 8px;
    background: #f5f5f5;
    display: block;
}

.instagram-feed__img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.instagram-feed__overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.instagram-feed__item:hover .instagram-feed__overlay {
    opacity: 1;
}

.instagram-feed__item:hover .instagram-feed__img {
    transform: scale(1.05);
}
"""

if ".instagram-feed__grid" not in css:
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(insta_css)
    print("Injected Instagram CSS")
