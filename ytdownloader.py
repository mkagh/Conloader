from pytube import YouTube
import tkinter as tk
from tkinter.filedialog import *
from tkinter import filedialog
import PySimpleGUI as sg
import moviepy.editor 

def createGui():
    layout=[[sg.Push(),sg.Button("enter",key='-ENTER-'),sg.Input(key="input")],
            [sg.Text("",key="-OUTCOME-")],
            [sg.Button("Nazad",key="-NAZAD-")]]
    return sg.Window("Yt Downloader",layout,size=(300,300),element_justification="center",resizable=True,finalize=True)

def createGuiforConvert():
    layout=[[sg.VPush(),sg.Button("covertPC",key='-CONVERTPC-'),
             sg.Button("covertWEB",key='-CONVERTWEB-')],
            [sg.Button("BACK",key='-BACK-')],
            [sg.Text("_______",key='-OUTCOME-')],
            [sg.Input("input",key="-INPUT-",disabled=True)],[sg.Button("submit",key="-SUBMIT-",disabled=True)]]
    return sg.Window("Yt Downloader",layout,size=(300,300),element_justification="center",resizable=True,finalize=True)

def main_menu():
    layout=[[sg.Push(),sg.Button("yto downloader",key='-YTD-'),sg.Button("convert",key="-CONVERT-")]]
    return sg.Window("Yt Downloader",layout,size=(300,300),element_justification="center",resizable=True,finalize=True)

def downloader(url,save_path,window):
    try:
        filename = sg.popup_get_text('Enter name:', 'Filename')
        filename=f"{filename}.mp4"
        if not url:
           sg.popup("must have url")
           return
        if not save_path:
           sg.popup("must have path")
           return
        if not filename:
           sg.popup("must have name")
           return
        else:
          yt=YouTube(url)
          streams=yt.streams.filter(progressive=True,file_extension="mp4")
          highest_res=streams.get_highest_resolution()
          highest_res.download(output_path=save_path,filename=filename)
          window["-OUTCOME-"].update("succsess")

    except Exception as e:
           print(e)
           window["-OUTCOME-"].update("fail you didnt enter something right")

def openfiledialog(): 
    folder=filedialog.askdirectory()
    return folder

root=tk.Tk()
root.withdraw()

def convertPC(video,save_dir,filename,window):
    try:    
        video=moviepy.editor.VideoFileClip(video)
        audio=video.audio
        output_path = f"{save_dir}\\{filename}.mp3"
        if not video:
           window["-OUTCOME-"].update("must provide video")
           return
        if not save_dir:
           window["-OUTCOME-"].update("must provide folder")
           return
        if not filename:
           window["-OUTCOME-"].update("must provide filename")
           return
        else:
           audio.write_audiofile(output_path)
           window["-OUTCOME-"].update("success")

    except Exception as e:
           window["-OUTCOME-"].update("something went wrong...")
   
window=main_menu()

def YTD(main_menu_window):
    window=createGui()
    while True:
     event,values=window.read()
     if event == sg.WIN_CLOSED:
        break
     if event == "-NAZAD-":
        window.close()
        main_menu_window.un_hide()
     if event == "-ENTER-":
      input_value = values['input']
      save_dir=openfiledialog()
      downloader(input_value,save_dir,window)

      window["input"].update("")

def Converter(main_menu_window):
    window=createGuiforConvert()
    while True:
     event,values=window.read()
     if event == sg.WIN_CLOSED:
        break
     if event == "-CONVERTPC-":
       video=askopenfilename()
       save_dir=openfiledialog()
       filename = sg.popup_get_text('Enter name:', 'Filename')
       
       convertPC(video,save_dir,filename,window)
          
     if event == "-CONVERTWEB-":
        window['-SUBMIT-'].update(disabled=False)
        window['-INPUT-'].update(disabled=False)
     if event == "-SUBMIT-":
        webvideo=values["-INPUT-"]
        save_dir=openfiledialog()
        filename = sg.popup_get_text('Enter name:', 'Filename')
        filename=f"{filename}.mp3"
        if not webvideo:
           window["-OUTCOME-"].update("must provide video VIA url")
           return
        if not save_dir:
           window["-OUTCOME-"].update("must provide folder")
           return
        if not filename:
           window["-OUTCOME-"].update("must provide filename")
           return
        else:
            try:
                yt = YouTube(webvideo)
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=save_dir,filename=filename)
                window["-OUTCOME-"].update("YOU DID IT")
            except Exception as e:
                window["-OUTCOME-"].update("SOMETHING WENT WRONG... ")
         
     
     
     if event == "-BACK-":
        window.close()
        main_menu_window.un_hide()

while True:
    event,values=window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == "-YTD-":
        window.hide() 
        YTD(window)
    if event == "-CONVERT-":
       window.hide() 
       Converter(window)

window.close()
if __name__ == "__main__":
    main_menu()
