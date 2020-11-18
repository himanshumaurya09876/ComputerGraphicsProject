#Egg cather game
# Import tools
from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font

# Canvas size
width_of_canvas=720
height_of_canvas=720
object_tkinter=Tk()

#Setting the canvas
c = Canvas(object_tkinter, width=width_of_canvas, height=height_of_canvas, background='sky blue')
c.create_rectangle(-5, height_of_canvas-100, width_of_canvas+5, height_of_canvas+5, fill='green', width=0)
c.create_oval(0,0,120,120,fill='yellow',width=0)
c.pack()

#Setting egg features
color_cycle = cycle(['blue','red','purple','white','orange'])
width_of_egg = 45
height_of_egg = 55
score_per_egg = 10
speed_of_egg = 500
egg_interval = 4000
difficulty_factor = 0.97

#Setting the bucket
bucket_color = 'black'
bucket_width = 100
bucket_height = 100
bucket_start_x = width_of_canvas/2 - bucket_width/2
bucket_start_y = height_of_canvas - bucket_height-20
bucket_start_x2 = bucket_start_x + bucket_width
bucket_start_y2 = bucket_start_y + bucket_height

#Creating the bucket
bucket = c.create_arc(bucket_start_x, bucket_start_y, bucket_start_x2, bucket_start_y2, start=200, extent=140, \
                       style='arc', outline=bucket_color, width=5)

#Setting the font/text
game_font = font.nametofont('TkTextFont')
game_font.config(size=14)

score=0
score_text = c.create_text(10,50,anchor='nw', font=game_font, fill='black', text='Score:'+str(score))

chances_remaining=5
chances_text = c.create_text(width_of_canvas-1, 10, anchor='ne',font=game_font,\
                          fill='black', text='Chances left: '+str(chances_remaining))

eggs = [] # Egg list

# Defining functions
def drop_eggs(): #Creates eggs
    x = randrange(10,700)
    y=40
    new_egg = c.create_oval(x,y,x+width_of_egg, y+height_of_egg, fill=next(color_cycle), width=0)
    eggs.append(new_egg) #add to the egg list
    object_tkinter.after(egg_interval,drop_eggs)
    
def move_eggs(): #to move eggs from top to bottom
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2)= c.coords(egg)
        c.move(egg,randrange(-5,5),10)
        if egg_y2 > height_of_canvas:
            egg_missed(egg)
    object_tkinter.after(speed_of_egg,move_eggs)
    
def egg_missed(egg): #if the egg is not caught in the bucket
    eggs.remove(egg) #remove it from list
    c.delete(egg) #remove it from canvas
    lost_a_chance()
    if chances_remaining == 0: #no chances left so game should be over now
        messagebox.showinfo('Game Over!', 'Final Score: '+str(score))
        object_tkinter.destroy()
        
def lost_a_chance(): #here chances are decreased by 1
    global chances_remaining
    chances_remaining-=1
    c.itemconfigure(chances_text, text='Chances left: '+str(chances_remaining))
    
def check_catch(): #after a fixed interval of time all eggs are checked if they are in bucket or not
    (bucket_x, bucket_y, bucket_x2, bucket_y2) = c.coords(bucket)
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2)= c.coords(egg)
        if bucket_x < egg_x and egg_x2 < bucket_x2 and bucket_y2 - egg_y2 < 40:#it means this egg is in bucket
            eggs.remove(egg) #so remove it from egg list
            c.delete(egg)#and remove it from canvas
            increase_score(score_per_egg) #increase the score for a caught
    object_tkinter.after(100,check_catch)
    
def increase_score(points): #if the egg is caught then
    global score, speed_of_egg, egg_interval
    score +=points #score is increased here
    speed_of_egg = int(speed_of_egg * difficulty_factor) #speed of egg is increased
    egg_interval = int(egg_interval* difficulty_factor) #eggs are created at faster rate
    c.itemconfigure(score_text, text='Score: '+str(score))
    
def move_left(event): #to control the movement of bucket
    (x1,y1,x2,y2) = c.coords(bucket)
    if x1 > 0:
        c.move(bucket, -20,0)
        
def move_right(event):#to control the movement of bucket
    (x1, y1,x2,y2) = c.coords(bucket)
    if x2<width_of_canvas:
        c.move(bucket,20,0)

#to bind the left and right arrow keys to the above functions, for movement of bucket
c.bind('<Left>',move_left)
c.bind('<Right>',move_right)
c.focus_set()

object_tkinter.after(1000,drop_eggs)
object_tkinter.after(1000,move_eggs)
object_tkinter.after(1000,check_catch)

object_tkinter.title("Egg Catcher Game")
object_tkinter.mainloop()