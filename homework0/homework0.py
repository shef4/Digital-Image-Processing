import cv2
import os

class Object_Detection():
    def __init__(self, path ,num_img):
        self.num_img = num_img
        self.path = path
        dir = os.listdir(path)
        img1 = None
        #read files from directoy
        for i,file in enumerate(dir):
            if file.endswith(".jpg"):
                file_path = f"{self.path}\{file}"
            img = cv2.imread(file_path)
            #collect 2 images then back subtract
            if (i+1)%2 != 0:
                img1 = img
            else: 
                img_set = (img1,img)
                title,img_output = self.background_sub(img_set)
                #self.print_img(title,img_output)
                self.save_img(f"Saved-Images\{title}--{file}",img_output)
            #stop when enough images collected
            if i == self.num_img*2-1: break
            
    def background_sub(self,img_set):
        img_res = []
        #convert to grey scale
        img1 = cv2.cvtColor(img_set[0], cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img_set[1], cv2.COLOR_BGR2GRAY)
        #compute absolute diffrence
        #img_res = cv2.absdiff(img1,img2)
        img_res = abs(img2-img1)
        return "Background_Subtraction",img_res
    
    def print_img(self,title, img):
        ZZZZZZZZZZZZZZZcv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return 
    
    def save_img(self,filename,img):
        cv2.imwrite(filename, img)
        return 

def main():
    Object_Detection("Walk1_jpg2\Walk1_jpg\JPEGS",100)

if __name__ == "__main__":
    main()