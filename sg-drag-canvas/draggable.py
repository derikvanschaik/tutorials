import PySimpleGUI as sg

def main():
    bott_left, top_right, centre = (0,0), (100,100), (50,50) 
    # main canvas 
    canvas = sg.Graph(
        (500, 500), bott_left, top_right, key='CANV',
        background_color='white',
        enable_events = True, 
         )
    # drag canvas - drag_submits parameter set to true 
    drag_canvas = sg.Graph(
        (500, 500), bott_left, top_right, key='DRAG-CANV', 
        background_color='white',
        enable_events = True, drag_submits= True 
         )
    # layout 
    output = sg.Text("", key="OUTPUT", size=(50, 1))    
    layout = [[output], [canvas, drag_canvas],]
    window = sg.Window('draggable graph application', layout) 
    # global event variables 
    figs = {} #key will be pysimple gui, maps to dict with 'selected' property 
    while(True):
        event, values = window.read()
        if event == "CANV": 
            click_location = values[event]
            # for else loop being used here 
            for figure in canvas.get_figures_at_location(click_location):
                # user clicked on present object 
                if figure in figs:
                    # toggle selected property 
                    figs[figure]['selected'] = not figs[figure]['selected']
                    # just some output text to let us know something is happening 
                    window['OUTPUT'].update(f"figure {figure} selected = {figs[figure]['selected']}")
                    break  
            # user is creating object     
            else:
                fig_id = canvas.draw_circle(click_location, radius = 5, fill_color = 'blue')
                figs[fig_id] = {'selected': False}
                # just some output text to let us know something is happening 
                window['OUTPUT'].update(f"Just created figure {fig_id}")

        if event == "DRAG-CANV":
            # just some output text to let us know something is happening
            drag_location = values[event] 
            window['OUTPUT'].update(f"USER is dragging on drag canvas at {drag_location}")  

        if event in(None, sg.WIN_CLOSED):  
            break 

    window.close() 
if __name__ == "__main__":
    main() 