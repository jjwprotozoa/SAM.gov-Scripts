import tkinter as tk  
import importrequestv3
import transform

def fetch_and_display():
    keyword = keyword_entry.get()
    set_aside = set_aside_entry.get()
    
    try:
        api_data = importrequestv3.fetch_api_data()
        opportunities = transform.process_opportunities(api_data) 
        filtered_opps = importrequestv3.filter_opportunities(opportunities, keyword, set_aside)
        
        # Display filtered opps in GUI
        display_opportunities(filtered_opps)
        
    except Exception as e:   
        messagebox.showerror("Error", str(e))
        
def export_to_csv():
    displayed_rows = get_displayed_opps()
    importrequestv3.save_csv(displayed_rows)

root = tk.Tk()

fetch_button = tk.Button(command=fetch_and_display)  
export_button = tk.Button(command=export_to_csv)

# Rest of GUI code

root.mainloop()