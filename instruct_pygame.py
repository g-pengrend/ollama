import pygame
import ollama
import threading

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 24)
screen = pygame.display.set_mode([800, 500])
timer = pygame.time.Clock()


# Function to format the chat history
def format_history(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = [{"role": "system", "content": system_prompt}]
    for query, response in history:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})
    chat_history.append({"role": "user", "content": msg})
    return chat_history

# Function to generate the LLM response
def generate_response(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = format_history(msg, history, system_prompt)
    response = ollama.chat(model='llama2', stream=True, messages=chat_history)
    message = ""
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        message += token
        yield message

# Function to wrap text within a given width
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    width, height = font.size('')

    for word in words:
        current_line.append(word)
        width, height = font.size(' '.join(current_line))
        if width > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))
    return lines

# Pygame input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dimgrey')
        self.color_active = pygame.Color('black')
        self.color = self.color_active
        self.text = text
        self.txt_surface = font.render(text, True, pygame.Color('white'))
        self.active = False
        self.prompt = "Ask a question"
        self.backspace_held = False
        self.backspace_timer = 0
        self.backspace_interval = 500  # milliseconds for initial delay
        self.backspace_repeat_rate = 50  # milliseconds for repeat rate

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    result = self.text
                    self.text = ''  # Clear the text
                    self.txt_surface = font.render(self.prompt, True, pygame.Color('grey'))
                    self.rect.w = max(200, self.txt_surface.get_width() + 10)
                    self.active = False
                    return result
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace_held = True
                    self.backspace_timer = pygame.time.get_ticks() + self.backspace_interval
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, pygame.Color('white'))
                self.rect.w = max(200, self.txt_surface.get_width() + 10)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = False    
        return None
    
    def update(self):
        if self.backspace_held and pygame.time.get_ticks() >= self.backspace_timer:
            self.text = self.text[:-1]
            self.txt_surface = font.render(self.text, True, pygame.Color('white'))
            self.rect.w = max(200, self.txt_surface.get_width() + 10)
            self.backspace_timer = pygame.time.get_ticks() + self.backspace_repeat_rate

    def draw(self, screen):
        if self.text == "" and not self.active:
            prompt_surface = font.render(self.prompt, True, pygame.Color('grey'))
            screen.blit(prompt_surface, (self.rect.x + 5, self.rect.y + 5))
        else:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Initialize variables
input_box = InputBox(10, 10, 780, 50)
message = ""
snip = font.render("", True, "white")
response_generator = None
response_text = ""
new_response = False
output_lines = []
output_box_rect = pygame.Rect(10, 100, 780, 380)
scroll_offset = 0
scroll_speed = 10

def fetch_response(text):
    global response_generator, new_response
    history = []  # you can update this with actual chat history if needed
    system_prompt = "Provide the answer clearly, in a short succinct way"  # Update with your system prompt
    response_generator = generate_response(text, history, system_prompt)
    new_response = True

# Main game loop
run = True
while run:
    screen.fill('darkgray')
    timer.tick(60)
    pygame.draw.rect(screen, 'black', output_box_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        result = input_box.handle_event(event)
        if result is not None:
            threading.Thread(target=fetch_response, args=(result,)).start()

        # Scroll with the mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            scroll_offset += event.y * scroll_speed

    input_box.update()
    input_box.draw(screen)

    if new_response:
        try:
            message = next(response_generator)
            output_lines = wrap_text(message, font, output_box_rect.width - 20)
        except StopIteration:
            new_response = False

    y_offset = output_box_rect.y + 10
    for line in output_lines:
        snip = font.render(line, True, 'white')
        screen.blit(snip, (output_box_rect.x + 10, y_offset))
        y_offset += snip.get_height() + 5

    pygame.display.flip()

pygame.quit()

# message = "This is a message"

# snip = font.render("", True, "white")
# counter = 0
# speed = 3
# done = False

# # main game loop
# run = True

# while run:
#     screen.fill('dark gray') # game background
#     timer.tick(60)
#     pygame.draw.rect(screen, 'black', [0,300,800,200]) # Just where i want to put the text

#     if counter < speed * len(message):
#         counter += 1
#     elif counter >= speed * len(message):
#         done = True

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     snip = font.render(message[0:counter//speed], True, 'white')
#     screen.blit(snip, (10,310))

#     pygame.display.flip()
# pygame.quit()