from PIL import Image
from glm import vec3
from time import perf_counter

print("Running program...")

tresh = 25


start = perf_counter()
Image.MAX_IMAGE_PIXELS = 1000000000

im = None
pixels = None
w = 0
h = 0



stint = lambda x: str(int(x))
zero = lambda x: "0" * (2 - len(stint(x))) + stint(x)

def ask(question):
    answer = ""
    while answer != "n" or answer != "y":
        answer = input(str(question)+" [y/n]").lower() 
        if answer == "y": return True
        elif answer == "n": return False
        else: print('Invalid input: Answer must be "y" or "n".')

def sec2time(x):
    seconds = x
    minutes = seconds // 60
    hours = minutes // 60

    seconds -= minutes*60
    minutes -= hours*60

    return f"{zero(hours)}:{zero(minutes)}:{zero(seconds)}"

def between(val, x, y):
    for i in range(3):
        
        if x[i] < y[i]:
            if x[i] <= val[i] <= y[i]:
                continue
            else: return False
        else:
            if y[i] <= val[i] <= x[i]:
                continue
            else: return False
    return True

def open_im(path):
    global im, pixels, w, h

    print("Opening "+path)


    im = Image.open(path)
    pixels = im.load()
    w, h = im.size

    print("File loaded.")




open_im("legend.png")
land = [vec3(pixels[w//2,y]) for y in range(h)]
print("Obtained colour profile.")


if ask("New file?"): open_im("map.jpeg")
else: open_im("ocean_map.png")
print("Drawing...")
total_changed = 0
estimations = []

for y in range(int(input("Start at: ")), h):
    round_time = perf_counter()
    changed = 0
    midpxl = vec3(pixels[w//2,y])
    if midpxl == vec3(0) or midpxl == vec3(255): continue
    for x in range(w):
        pxl = vec3(pixels[x,y])
        if pxl != vec3(255):
            for i in range(len(land)-1):
                if between(pxl, land[i], land[i+1]):
                    pixels[x,y] = (255,255,255)
                    changed += 1

#        if between(pxl,vec3(pxl.b+tresh, pxl.b+tresh, pxl.b),vec3(255)) and pxl != vec3(255):
#            pixels[x,y] = (255,255,255)
#            changed += 1

    estimated = (perf_counter() - round_time)
    estimations.append(estimated)
    for est in estimations: estimated += est
    estimated /= len(estimations)
    estimated *= (h - y - 1)

    print(f"Changed {changed} pixels on line {y+1}/{h} - Estimated time: {sec2time(estimated)}")
    total_changed += changed

    if (y+1)%100 == 0 and total_changed > 0:
        print("Autosaving...")
        im.save("ocean_map.png")
        print("Saved.")



print(f"Modified {total_changed} out of {w*h} pixels.")




print("Saving...")
im.save("ocean_map.png")
print("Saved result.")



delay = round(perf_counter()-start)
print(f"Finished program in {sec2time(delay)}")
