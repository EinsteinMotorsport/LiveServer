

class Logfile(object):

    def WriteFile(slef,id,zeit,wert):
        text=str(id)+'~'+str(zeit)+'~'+str(wert)+'\r\n'
        f = open('Logenfle.txt', 'a')
        f.write(text)
        f.close()


    def OpenFile(self):

        with open('Logenfle.txt') as f:
            content = f.read().splitlines()
        for i in content:
            if i == '':
              content.remove(i)
        # close the file after reading the lines.
        f.close()
        return content

    def deleteContent(self,fName):
        with open(fName, "w"):
            pass

    def main(self):
         Logfile.WriteFile(self, 4, 5, 6)
         Logfile.WriteFile(self, 6, 5, 7)
         Logfile.WriteFile(self, 5, 5, 5)
         Logfile.WriteFile(self, 3, 5, 3)
         #Logfile.deleteContent(self, 'Logenfle.txt')
         print(Logfile.OpenFile(self))


if __name__ == '__main__':

    Logfile.main(object)