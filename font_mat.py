import matplotlib.font_manager

unformatted_fonts_path_list = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
formatted_fonts_path_list = [x.split("\\")[-1] for x in unformatted_fonts_path_list]
fonts_list = [x.split("/")[-1].split(".")[:-1][0] for x in formatted_fonts_path_list]
fonts_list.sort()
print(fonts_list)
# print(formatted_fonts_path_list.__len__())

# fonts_dict = {k:v for (k,v) in zip(fonts_list, formatted_fonts_path_list)}
# a = list(fonts_dict.keys())
# print(a)