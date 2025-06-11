import sounddevice as sd

devices = sd.query_devices()
default = sd.default.device

print("\n🎙️ Lista de dispositivos:")
for i, d in enumerate(devices):
    print(f"{i}: {d['name']} - input channels: {d['max_input_channels']}")

print("\n🔧 Dispositivo por defecto:", default)
