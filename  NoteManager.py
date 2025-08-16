
class NoteManager:

    notes = []
    
    def add(self, note):

        self.notes.append(note)

    def edit(self,index, new_note):

        self.notes[index] = new_note

    def remove(self, index):

        del self.notes[index]

