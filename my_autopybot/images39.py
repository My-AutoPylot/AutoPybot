import os
from my_autopybot.CrashHandler import report_error

output_folder = os.path.join(
    os.path.abspath(r'C:\Users\Public\PyBots'), 'My-autopybot', 'Images Folder')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def camera_capture_image(folder_path="", file_name=""):
    """
    Description:
        Capture an image from the camera and save it to the given folder path.
    Args:
        folder_path (str): The folder path to save the image.
        file_name (str): The file name to save the image.
    Returns:
        [status]
        status (bool): Whether the function is successful or failed.
    """
    # Import Section
    import cv2
    import numpy as np
    from my_autopybot.CrashHandler import report_error
    import time
    from pathlib import Path
    import datetime

    # Response Section
    status = False

    try:
        if not folder_path:
            folder_path = output_folder
        if not file_name:
            file_name = "image_" + \
                str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + ".png"
        SECONDS = 5
        TIMER = int(SECONDS)
        window_name = "PyBOTs"
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            raise Exception("Error in Opening Camera")

        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # while True:
        ret, img = cap.read()
        cv2.imshow(window_name, img)
        prev = time.time()

        text = "Saving image in 5 second(s)"
        textsize = cv2.getTextSize(text, font, 1, 2)[0]
        # print(str(textsize))

        textX = int((img.shape[1] - textsize[0]) / 2)
        textY = int((img.shape[0] + textsize[1]) / 2)

        while TIMER >= 0:
            ret, img = cap.read()

            cv2.putText(img, "Saving image in {} second(s)".format(str(TIMER)),
                        (textX, textY), font,
                        1, (255, 0, 255),
                        2)
            cv2.imshow(window_name, img)
            cv2.waitKey(125)

            cur = time.time()

            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1

        if not file_name:
            file_name = "image_" + \
                str(datetime.datetime.now().strftime(
                    "%d%m%Y_%h:%m:%s")) + ".png"

        ret, img = cap.read()
        cv2.imshow(window_name, img)
        cv2.waitKey(1000)
        file_path = str(os.path.join(folder_path, file_name))
        cv2.imwrite(file_path, img)

        cap.release()
        cv2.destroyAllWindows()

        os.startfile(file_path)

    except Exception as ex:
        report_error(ex)

    else:
        status = True

    finally:
        return [status]


def crop_document_from_image(input_image_path="", output_folder_path=""):

    # Description:
    # """
    # Description:
    #     Exports the document from the image. by cropping out the biggest contour and applying the transformation

    # Args:
    #     input_image_path (str): The path of the image to be processed
    #     output_folder_path (str): The path of the folder where the output image will be saved

    # Returns:
    #     [bool]: Whether the function is successful or failed.

    # """

    # import section

    from pathlib import Path
    import os
    import numpy as np
    import cv2
    import re
    from matplotlib import pyplot as plt
    import sys
    # Hellper section
    # ## **Use Gaussian Blurring combined with Adaptive Threshold**

    def blur_and_threshold(gray):
        gray = cv2.GaussianBlur(gray, (3, 3), 2)
        threshold = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        threshold = cv2.fastNlMeansDenoising(threshold, 11, 31, 9)
        return threshold
    # ## **Find the Biggest Contour**
    # **Note: We made sure the minimum contour is bigger than 1/10 size of the whole picture. This helps in removing very small contours (noise) from our dataset**

    def biggest_contour(contours, min_area):
        biggest = None
        max_area = 0
        biggest_n = 0
        approx_contour = None
        for n, i in enumerate(contours):
            area = cv2.contourArea(i)

            if area > min_area/10:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02*peri, True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area
                    biggest_n = n
                    approx_contour = approx

        return biggest_n, approx_contour

    def order_points(pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        pts = pts.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect
    # ## Find the exact (x,y) coordinates of the biggest contour and crop it out

    def four_point_transform(image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth + 10, 0],
            [maxWidth + 10, maxHeight + 10],
            [0, maxHeight + 10]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        # return the warped image
        return warped
    # # Transformation the image
    # **1. Convert the image to grayscale**

    # **2. Remove noise and smoothen out the image by applying blurring and thresholding techniques**

    # **3. Use Canny Edge Detection to find the edges**

    # **4. Find the biggest contour and crop it out**
    def transformation(image1):
        image = image1.copy()
        height, width, channels = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_size = gray.size

        threshold = blur_and_threshold(gray)
        # We need two threshold values, minVal and maxVal. Any edges with intensity gradient more than maxVal
        # are sure to be edges and those below minVal are sure to be non-edges, so discarded.
        #  Those who lie between these two thresholds are classified edges or non-edges based on their connectivity.
        # If they are connected to "sure-edge" pixels, they are considered to be part of edges.
        #  Otherwise, they are also discarded
        edges = cv2.Canny(threshold, 50, 150, apertureSize=7)
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        simplified_contours = []

        for cnt in contours:
            hull = cv2.convexHull(cnt)
            simplified_contours.append(cv2.approxPolyDP(hull,
                                                        0.001*cv2.arcLength(hull, True), True))
        simplified_contours = np.array(simplified_contours, dtype=object)
        biggest_n, approx_contour = biggest_contour(
            simplified_contours, image_size)

        threshold = cv2.drawContours(
            image, simplified_contours, biggest_n, (0, 255, 0), 1)

        dst = 0
        if approx_contour is not None and len(approx_contour) == 4:
            approx_contour = np.float32(approx_contour)
            dst = four_point_transform(threshold, approx_contour)
        croppedImage = dst
        return croppedImage
    # **Increase the brightness of the image by playing with the "V" value (from HSV)**

    def increase_brightness(img, value=30):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    # **Sharpen the image using Kernel Sharpening Technique**

    def final_image(rotated):
        # Create our shapening kernel, it must equal to one eventually
        kernel_sharpening = np.array([[0, -1, 0],
                                      [-1, 5, -1],
                                      [0, -1, 0]])
        # applying the sharpening kernel to the input image & displaying it.
        sharpened = cv2.filter2D(rotated, -1, kernel_sharpening)
        sharpened = increase_brightness(sharpened, 30)
        return sharpened

    def enhance_the_image_document(input_image_path="", output_folder_path=""):

        # Description:
        """
        Description:
            This function takes an image as input and crops out the document from the image by cropping out the biggest contour and applying the transformation from the folder 

        Args:
            input_folder_path (str): The path of the folder where the images are present
            output_folder_path (str): The path of the folder where the output image will be saved

        Returns:
            [bool,List]: Whether the function is successful or failed. and the list of the images that are processed
        """

        # import section

        from pathlib import Path
        import os

        # Response section
        status = False
        # Logic section
        try:

            if not input_image_path:
                raise Exception("Enter the valid input image path")
            if not output_folder_path:
                raise Exception("Enter the valid output image path")

            img = cv2.imread(input_image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # do morph-dilate-op
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilated = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)
            diff1 = 255 - cv2.subtract(dilated, gray)

            # do medianBlur
            median = cv2.medianBlur(dilated, 15)
            diff2 = 255 - cv2.subtract(median, gray)

            # do normalize
            normed = cv2.normalize(diff2, None, 0, 255, cv2.NORM_MINMAX)
            basename = os.path.basename(input_image_path)

            # save the result
            # dst = np.hstack((gray, normed))
            cv2.imwrite(output_folder_path + basename, normed)
    #         res = np.hstack((gray,dilated, diff1,  median, diff2, normed))
    #         cv2.imwrite(output_folder_path + "exported2_"+basename, res)

            status = True

        except Exception as ex:
            print(ex)

        else:
            status = True
        finally:
            return [status]

        # ## 1. Pass the image through the transformation function to crop out the biggest contour

        # ## 2. Brighten & Sharpen the image to get a final cleaned image

    # Response section
    status = False

    # Logic section
    try:
        if not input_image_path:
            raise Exception("Enter the valid input image path")
        if not output_folder_path:
            output_folder_path = output_folder

        filename = os.path.join(
            output_folder_path, str(Path(input_image_path).stem) + ".jpg")

        image = cv2.imread(input_image_path)
        # print(image)
        # blurred_threshold = transformation(image)
        # print(blurred_threshold)
        cleaned_image = final_image(image)

        print(filename)
        cv2.imwrite(filename, cleaned_image)
        enhance_the_image_document(
            filename, output_folder_path)

        status = True
        os.startfile(output_folder_path)

    except Exception as ex:
        line_number = sys.exc_info()[-1].tb_lineno
        print(line_number)
        # print(str(e.args))
        # report_error(ex)

    else:
        status = True
    finally:
        return [status]


def crop_document_from_image_folder(input_folder_path="", output_folder_path=""):

    # Description:
    """
    Description:
        crops out the document from the image. by cropping out the biggest contour and applying the transformation from the folder

    Args:
        input_folder_path (str): The path of the folder where the images are present
        output_folder_path (str): The path of the folder where the output image will be saved

    Returns:
        [bool,List]: Whether the function is successful or failed. and the list of the images that are processed
    """

    # import section

    from pathlib import Path
    import os
    import numpy as np
    import cv2
    import re
    from matplotlib import pyplot as plt
    # Hellper section
    # ## **Use Gaussian Blurring combined with Adaptive Threshold**

    def blur_and_threshold(gray):
        gray = cv2.GaussianBlur(gray, (3, 3), 2)
        threshold = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        threshold = cv2.fastNlMeansDenoising(threshold, 11, 31, 9)
        return threshold

    # ## **Find the Biggest Contour**
    # **Note: We made sure the minimum contour is bigger than 1/10 size of the whole picture. This helps in removing very small contours (noise) from our dataset**
    def biggest_contour(contours, min_area):
        biggest = None
        max_area = 0
        biggest_n = 0
        approx_contour = None
        for n, i in enumerate(contours):
            area = cv2.contourArea(i)

            if area > min_area/10:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02*peri, True)
                if area > max_area and len(approx) == 4:
                    biggest = approx
                    max_area = area
                    biggest_n = n
                    approx_contour = approx

        return biggest_n, approx_contour

    def order_points(pts):
        # initialzie a list of coordinates that will be ordered
        # such that the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        pts = pts.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect
    # ## Find the exact (x,y) coordinates of the biggest contour and crop it out

    def four_point_transform(image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        rect = order_points(pts)
        (tl, tr, br, bl) = rect

        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth + 10, 0],
            [maxWidth + 10, maxHeight + 10],
            [0, maxHeight + 10]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        # return the warped image
        return warped
    # # Transformation the image
    # **1. Convert the image to grayscale**

    # **2. Remove noise and smoothen out the image by applying blurring and thresholding techniques**

    # **3. Use Canny Edge Detection to find the edges**

    # **4. Find the biggest contour and crop it out**
    def transformation(image):
        image = image.copy()
        height, width, channels = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_size = gray.size

        threshold = blur_and_threshold(gray)
        # We need two threshold values, minVal and maxVal. Any edges with intensity gradient more than maxVal
        # are sure to be edges and those below minVal are sure to be non-edges, so discarded.
        #  Those who lie between these two thresholds are classified edges or non-edges based on their connectivity.
        # If they are connected to "sure-edge" pixels, they are considered to be part of edges.
        #  Otherwise, they are also discarded
        edges = cv2.Canny(threshold, 50, 150, apertureSize=7)
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        simplified_contours = []

        for cnt in contours:
            hull = cv2.convexHull(cnt)
            simplified_contours.append(cv2.approxPolyDP(hull,
                                                        0.001*cv2.arcLength(hull, True), True))
        simplified_contours = np.array(simplified_contours, dtype=object)
        biggest_n, approx_contour = biggest_contour(
            simplified_contours, image_size)

        threshold = cv2.drawContours(
            image, simplified_contours, biggest_n, (0, 255, 0), 1)

        dst = 0
        if approx_contour is not None and len(approx_contour) == 4:
            approx_contour = np.float32(approx_contour)
            dst = four_point_transform(threshold, approx_contour)
        croppedImage = dst
        return croppedImage
    # **Increase the brightness of the image by playing with the "V" value (from HSV)**

    def increase_brightness(img, value=30):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    # **Sharpen the image using Kernel Sharpening Technique**

    def final_image(rotated):
        # Create our shapening kernel, it must equal to one eventually
        kernel_sharpening = np.array([[0, -1, 0],
                                      [-1, 5, -1],
                                      [0, -1, 0]])
        # applying the sharpening kernel to the input image & displaying it.
        sharpened = cv2.filter2D(rotated, -1, kernel_sharpening)
        sharpened = increase_brightness(sharpened, 30)
        return sharpened

    def enhance_the_image_document(input_image_path="", output_folder_path=""):

        # Description:
        """
        Description:
            Crops out the document from the image. by cropping out the biggest contour and applying the transformation from the folder

        Args:
            input_folder_path (str): The path of the folder where the images are present
            output_folder_path (str): The path of the folder where the output image will be saved

        Returns:
            [bool,List]: Whether the function is successful or failed. and the list of the images that are processed
        """

        # import section

        from pathlib import Path
        import os

        # Response section
        status = False
        # Logic section
        try:

            if not input_image_path:
                raise Exception("Enter the valid input image path")
            if not output_folder_path:
                raise Exception("Enter the valid output image path")

            img = cv2.imread(input_image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # do morph-dilate-op
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilated = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)
            diff1 = 255 - cv2.subtract(dilated, gray)

            # do medianBlur
            median = cv2.medianBlur(dilated, 15)
            diff2 = 255 - cv2.subtract(median, gray)

            # do normalize
            normed = cv2.normalize(diff2, None, 0, 255, cv2.NORM_MINMAX)
            basename = os.path.basename(input_image_path)

            # save the result
            # dst = np.hstack((gray, normed))
            cv2.imwrite(output_folder_path + basename, normed)
    #         res = np.hstack((gray,dilated, diff1,  median, diff2, normed))
    #         cv2.imwrite(output_folder_path + "exported2_"+basename, res)

            status = True

        except Exception as ex:
            print(ex)

        else:
            status = True
        finally:
            return [status]

        # ## 1. Pass the image through the transformation function to crop out the biggest contour

        # ## 2. Brighten & Sharpen the image to get a final cleaned image

    # Response section
    status = False
    exported = []
    # Logic section
    try:

        if not input_folder_path:
            raise Exception("Enter the valid input image path")
        if not output_folder_path:
            raise Exception("Enter the valid output image path")

        valid_formats = [".jpg", ".jpeg", ".png"]
        def get_text(f): return os.path.splitext(f)[1].lower()
        img_files = [input_folder_path + f for f in os.listdir(
            input_folder_path) if get_text(f) in valid_formats]

        for imagefile in img_files:

            image = cv2.imread(imagefile)

            blurred_threshold = transformation(image)
            cleaned_image = final_image(blurred_threshold)
            basename = os.path.basename(imagefile)

            cv2.imwrite(output_folder_path + "exported_" +
                        basename, cleaned_image)
            enhance_the_image_document(
                output_folder_path + "exported_"+basename, output_folder_path)
            exported.append("exported_"+basename)

        status = True

    except Exception as ex:
        print(ex)

    else:
        status = True
    finally:
        return [status, exported]


def enhance_the_image_document(input_image_path="", output_folder_path=""):

    # Description:
    """
    Description:
        Crops out the document from the image. by cropping out the biggest contour and applying the transformation from the folder

    Args:
        input_folder_path (str): The path of the folder where the images are present
        output_folder_path (str): The path of the folder where the output image will be saved

    Returns:
        [bool,List]: Whether the function is successful or failed. and the list of the images that are processed
    """

    # import section
    import os
    import cv2

    # Response section
    status = False
    # Logic section
    try:

        if not input_image_path:
            raise Exception("Enter the valid input image path")
        if not output_folder_path:
            raise Exception("Enter the valid output image path")

        img = cv2.imread(input_image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # do morph-dilate-op
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated = cv2.morphologyEx(gray, cv2.MORPH_DILATE, kernel)
        diff1 = 255 - cv2.subtract(dilated, gray)

        # do medianBlur
        median = cv2.medianBlur(dilated, 15)
        diff2 = 255 - cv2.subtract(median, gray)

        # do normalize
        normed = cv2.normalize(diff2, None, 0, 255, cv2.NORM_MINMAX)
        basename = os.path.basename(input_image_path)

        # save the result
        # dst = np.hstack((gray, normed))
        cv2.imwrite(output_folder_path + "Enhanced_"+basename, normed)
#         res = np.hstack((gray,dilated, diff1,  median, diff2, normed))
#         cv2.imwrite(output_folder_path + "exported2_"+basename, res)

        status = True

    except Exception as ex:
        print(ex)

    else:
        status = True
    finally:
        return [status]


# crop_document_from_image(r"C:\Users\PyBots\Desktop\documents\5.jpeg")
# crop_document_from_image_folder(r"C:\Users\PyBots\Desktop\documents")
