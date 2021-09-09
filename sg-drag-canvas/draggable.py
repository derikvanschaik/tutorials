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
        
    # wrap each canvas into a tab 
    main_tab = sg.Tab("dragging off", [[canvas]]) 
    drag_tab = sg.Tab("dragging on", [[drag_canvas]], visible=False) # dragging tab is invisible 
    # create tab group 
    tabs = sg.TabGroup([[main_tab, drag_tab]])
    # create drag mode toggler button 
    # set metadata parameter to false. True -> in drag mode False -> not in drag mode 
    mode_toggler = sg.Button("toggle drag mode", metadata=False ) 
    # layout 
    output = sg.Text("", key="OUTPUT", size=(50, 1))    
    layout = [[output, mode_toggler], [tabs]]
    window = sg.Window('draggable graph application', layout)    

    # global event variables 
    figs = {} #key will be pysimple gui, maps to dict with 'selected' property 
    twin_tracker = {} # maps canvas objects to drag canvas objects and vice versa  
    while(True):
        event, values = window.read()
        if event in(None, sg.WIN_CLOSED):  
            break 
        elif event == "CANV": 
            click_location = values[event] 
            # for else loop being used here 
            for figure in canvas.get_figures_at_location(click_location): 
                # toggle selected property 
                figs[figure]['selected'] = not figs[figure]['selected'] 
                # just some output text to let us know something is happening 
                window['OUTPUT'].update(f"figure {figure} selected = {figs[figure]['selected']}")
                break  
            # user is creating object     
            else:
                fig_id = canvas.draw_circle(click_location, radius = 5, fill_color = 'blue')
                figs[fig_id] = {'selected': False, 'location': click_location} 
                # create figure to be drawn onto drag canvas 
                drag_fig_id = drag_canvas.draw_circle(click_location, radius = 5, fill_color = 'blue')
                # map figures to eachother 
                twin_tracker[fig_id] = drag_fig_id
                twin_tracker[drag_fig_id] = fig_id 

        elif event == "DRAG-CANV":  
            # drag location x and y 
            (x, y) = values[event]
            # threshold for fig drags (hotspot)
            thresh = 5 
            for fig_id, fig_obj  in figs.items():
                fig_x, fig_y = fig_obj['location']
                # user is dragging this figure 
                if (abs(x-fig_x) <= thresh and abs(y-fig_y) <= thresh): 
                    canvas.relocate_figure(fig_id, x, y) 
                    drag_canvas.relocate_figure( twin_tracker[fig_id], x, y) 
                    fig_obj['location'] = (x, y) # reset new location
                    break 
        
        elif event == "toggle drag mode":
            # toggle drag mode 
            mode_toggler.metadata = not mode_toggler.metadata 
            dragging = mode_toggler.metadata 
            # toggle visibility properties of tabs -- only show one at a time 
            window['dragging on'].update( visible = dragging) 
            window['dragging off'].update( visible = not dragging)
            # select original canvas if not in dragging mode. 
            if not dragging:
                      window['dragging off'].select()  


    window.close() 
if __name__ == "__main__":
    main() 
