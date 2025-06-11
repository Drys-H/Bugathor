import qrcode

url = "https://bugathor.onrender.com/"

img = qrcode.make(url)

img.save("bugathor_qr.png")

print("QR code generated and saved as bugathor_qr.png")