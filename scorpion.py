
import sys
import exiftool

for arg in sys.argv[1:]:
	
		print("Metadata for image:", arg)
		print("-------------")
		with exiftool.ExifToolHelper() as et:
			metadata = et.get_metadata(arg)
		for item in metadata:
			for key, value in item.items():
				print(f"{key}: {value}")
				print()
