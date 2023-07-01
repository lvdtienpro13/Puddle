
from django.shortcuts import render, redirect
from .forms import ImageSearchForm
from ml.search_image import search_item_by_image
from item.models import Item
from django.core.files.images import ImageFile
from django.db.models import Q

from django.conf import settings
import os

def search_item(request):
    if request.method == 'POST':
        form = ImageSearchForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            list_path = search_item_by_image(image_file)
            print(list_path)
            items = []
            for path in list_path:
                # Truy vấn cơ sở dữ liệu để lấy id_item dựa trên đường dẫn ảnh
                try:
                    new_path = path[0]
                    new_path = new_path.replace('\\', '/')
                    new_path = new_path.replace('../media/', '')
                    print(new_path)
                    item = Item.objects.filter(image=new_path).first()
                    if item is not None:
                        items.append(item)
                        print(type(item))
                        print(item.name)
                    else:
                        pass
                except Item.DoesNotExist:
                    print("khong tim thay")
                    # Xử lý trường hợp không tìm thấy đường dẫn ảnh trong cơ sở dữ liệu
                    pass
            print(len(items))
            context = {
                'form': form,
                'items': items,
            }
            return render(request, 'searchbyimage/searchbyimage.html', context=context)
    else:
        form = ImageSearchForm()

    return render(request, 'searchbyimage/searchbyimage.html', {'form': form})

# def search_item(request):

#     print(search_item_by_image("C:/Users/KimAnh/Desktop/PUDDLE/puddle/ml/test_images/317998465_1228741551326443_6125795881385636226_n.jpg"))
#     items = []
#     id_items = []
#     list_path = search_item_by_image("C:/Users/KimAnh/Desktop/PUDDLE/puddle/ml/test_images/317998465_1228741551326443_6125795881385636226_n.jpg")
    # for path in list_path:
    #     # Truy vấn cơ sở dữ liệu để lấy id_item dựa trên đường dẫn ảnh
    #     try:
    #         new_path = path[0]
    #         print(new_path)
    #         new_path = new_path.replace('\\', '/')
    #         new_path = new_path.replace('../media', '')
    #         # media_path = str(settings.MEDIA_ROOT)
    #         # media_path = media_path.replace("\\",'/')
    #         # new_path = media_path+new_path
    #         # print(new_path)
    #         # new_path = os.path.join(settings.MEDIA_ROOT, new_path )
    #         # image_file = ImageFile(open(new_path, 'rb'))

    #         # item = Item.objects.get(image=image_file)
    #         item = Item.objects.filter(image=new_path).first()
            
    #         #id_item = item.name
    #         # Thêm đặc trưng và id_item vào danh sách
    #         #id_items.append(id_item)
    #         items.append(item)
    #     except Item.DoesNotExist:
    #         print("khong tim thay")
    #         # Xử lý trường hợp không tìm thấy đường dẫn ảnh trong cơ sở dữ liệu
    #         pass
    # #print(id_items)
    # print(len(items))
    # item1 = Item.objects.get(id = 2)
    # print(item1.image)
    # print(type(item1.image))
    # return render(request, 'searchbyimage/searchbyimage.html')
