#Persistent  ; Keep the script running persistently

; Define hotkeys
^+i::InsertImages()  ; Ctrl + Shift + I to trigger the insertion process
^+p::PauseScript()   ; Ctrl + Shift + P to pause/override the script
^+l::LoopInsertImages()  ; Ctrl + Shift + L to loop the insertion process 10 times
^+r::Reload
^+q::Reload


LoopInsertImages() {
    Loop, 1000 {  ; Loop 10 times
        InsertImages()
        Sleep 1000  ; Add a delay between each iteration (optional)
    }
}

InsertImages() {
    ; Click on the specified mouse position (replace with your coordinates)
    SetKeyDelay, 100 
    SetMouseDelay, 50

    Send {Right 2}
    Send ^c
    Send {Left 2}
    ; Send Ctrl + c to copy the selected content

    MouseMove 205, 170 ; Insert
    Sleep 500
    Click
    MouseMove 341, 410 ; Image
    Sleep 500
    MouseMove 633, 418 ; Insert image in cell
    Sleep 500
    Click
    MouseMove 704, 293 ; Google Drive
    Sleep 500
    Click
    MouseMove 739, 227 ; Search Bar
    Sleep 500
    Click
    
    Send ^v ; Paste
    Send {Enter} 

    MouseMove 460, 363 ; Select Image
    Sleep 1000
    Click
    Sleep 1000

    target_color :=0xE8731A
    PixelGetColor pixel_color, 1500, 931

    while (pixel_color != target_color) {
        ; ToolTip, % "Pixel color: " . pixel_color
        Click
        Sleep 1000
        PixelGetColor pixel_color, 1500, 931
    }

    Click 1500, 931 ; Insert


    Sleep 100
    Send {Down}
}

PauseScript() {
    ; Toggle pause state of the script
    Suspend, Toggle
}
