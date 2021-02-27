
class emulatedDisk:
    
    def __init__(self):
        self.byteArray = [bytearray(512) for i in range(64)]
        self.inputBuffer = bytearray(512)
        self.outputBuffer = bytearray(512)
        self.M = bytearray(512)
        self.OFT = [[bytearray(512), -1, 0, 0] for i in range(4)]
        self.OFT[0][1] = 0
        self.OFT[0][3] = 0
        
        for i in range(64):
            for j in range(512):
                self.byteArray[i][j] = 0
        
        emulatedDisk.setBytesToInt(self,self.byteArray, 1,0,512)
        emulatedDisk.setBytesToInt(self,self.byteArray, 1,4,7)
#         counter = 0
#         while counter < 9:
#             self.byteArray[0][counter] = 0
#             counter += 1
#             
        for i in range(1,7):
            for j in range(0,512,16):
                if j != 0:
                    emulatedDisk.setBytesToInt(self,self.byteArray, i,j,4294967295)
#         
#         self.byteArray[1][0] = 0
#         self.byteArray[1][1] = 0
#         self.byteArray[1][2] = 0
#         self.byteArray[1][3] = 0
#         self.byteArray[1][7]  = 0

    def setBytesToInt(self, byArr,block,position,num):
        bytesNum = num.to_bytes(4, 'big')
        byArr[block][position] = bytesNum[0]
        byArr[block][position+1] = bytesNum[1]
        byArr[block][position+2] = bytesNum[2]
        byArr[block][position+3] = bytesNum[3]
        
    def setBytesToInt2(self, byArr,position,num):
        bytesNum = num.to_bytes(4, 'big')
        byArr[position] = bytesNum[0]
        byArr[position+1] = bytesNum[1]
        byArr[position+2] = bytesNum[2]
        byArr[position+3] = bytesNum[3]
        
    def getIntFromBytes(self, byArr,block,position):
        intFromBytes = int.from_bytes(byArr[block][position:position+4], byteorder='big', signed=True)
        return intFromBytes
    
    def getIntFromBytes2(self, byArr,position):
        intFromBytes = int.from_bytes(byArr[position:position+4], byteorder='big', signed=True)
        return intFromBytes
    
    def compareByName(self, byArr, block, position, str):
        arrStringBytes = bytes(str, 'utf-8');
        if (arrStringBytes[0] == byArr[position] and arrStringBytes[1] == byArr[position+1] and arrStringBytes[2] == byArr[position+2] ):
            return True
        return False
    
    def compareByName2(self, byArr, position, str1):
        arrStringBytes = bytes(str1, 'utf-8');
        if(len(str1) == 3):
            if (arrStringBytes[0] == byArr[position] and arrStringBytes[1] == byArr[position+1] and arrStringBytes[2] == byArr[position+2] ):
                return True
        if(len(str1) == 2):
            if (arrStringBytes[0] == byArr[position] and arrStringBytes[1] == byArr[position+1] ):
                return True
        if(len(str1) == 1):
            if (arrStringBytes[0] == byArr[position] ):
                return True
        return False
        
    def create(self, name):
#         print(emulatedDisk.toString(self))
        #duplicates to do
        for j in range(0,512,8):
            emulatedDisk.seek(self,0,j)
            if emulatedDisk.compareByName2(self, self.OFT[0][0], self.OFT[0][1], name):
                return False
        #search for free file descriptor
        availableFileDescriptorIndex = -1
        exit = False
        for i in range(1,7):
            for j in range(0,512,16):
                if emulatedDisk.getIntFromBytes(self,self.byteArray, i,j) == -1:
                    emulatedDisk.setBytesToInt(self,self.byteArray, i,j,0)  
                    availableFileDescriptorIndex = (int) (j/16+(32*(i-1)))
                    exit = True
                    break
            if exit:
                break
#         print(availableFileDescriptorIndex)
        if availableFileDescriptorIndex == -1:
            return False
        fdBlock =(int) (((availableFileDescriptorIndex * 16) / 512) +1)
        descriptorPos = ((availableFileDescriptorIndex * 16) % 512)
        directorySize = emulatedDisk.getIntFromBytes(self,self.byteArray,fdBlock,descriptorPos)
        for j in range(0,512,8):
#             emulatedDisk.setBytesToInt(self,self.byteArray, fdBlock,descriptorPos, directorySize+16)
            emulatedDisk.seek(self,0,j)
            if emulatedDisk.getIntFromBytes2(self,self.OFT[0][0],self.OFT[0][1]+4) == 0:
                
                arrStringBytes = bytes(name, 'utf-8')
                self.byteArray[7][j] = arrStringBytes[0]
                if len(name) > 1:
                    self.byteArray[7][j+1] = arrStringBytes[1]
                if len(name) > 2:
                    self.byteArray[7][j+2] = arrStringBytes[2]
                self.OFT[0][0][self.OFT[0][1]] = arrStringBytes[0]
                if len(name) > 1:
                    self.OFT[0][0][self.OFT[0][1]+1] = arrStringBytes[1]
                if len(name) > 2:
                    self.OFT[0][0][self.OFT[0][1]+2] = arrStringBytes[2]
                emulatedDisk.setBytesToInt(self,self.byteArray, 7,self.OFT[0][1]+4,availableFileDescriptorIndex)
                emulatedDisk.setBytesToInt2(self, self.OFT[0][0],self.OFT[0][1]+4, availableFileDescriptorIndex)
                break                                       
#         print(emulatedDisk.toString(self))
        return True            
    
    def destroy(self, name):
        fileDescriptorOldIndex = -1
        for j in range(0,512,8):
            emulatedDisk.seek(self,0,j)
            if emulatedDisk.compareByName2(self, self.OFT[0][0], self.OFT[0][1], name):
                fileDescriptorOldIndex = emulatedDisk.getIntFromBytes2(self, self.OFT[0][0], self.OFT[0][1]+4)
                emulatedDisk.setBytesToInt(self,self.byteArray, 7,self.OFT[0][1]+4,0) 
                emulatedDisk.setBytesToInt2(self,self.OFT[0][0], self.OFT[0][1]+4,0) 
                break
        if  (fileDescriptorOldIndex == -1):
            return False
        fdBlock = (int) (((fileDescriptorOldIndex * 16) / 512) +1)
        descriptorPos = (int) ((fileDescriptorOldIndex * 16) % 512)  
        emulatedDisk.setBytesToInt(self,self.byteArray, fdBlock,descriptorPos,4294967295) 
        emulatedDisk.setBytesToInt(self,self.byteArray, fdBlock,descriptorPos+4,0) 
        emulatedDisk.setBytesToInt(self,self.byteArray, fdBlock,descriptorPos+8,0) 
        emulatedDisk.setBytesToInt(self,self.byteArray, fdBlock,descriptorPos+12,0) 
        return True
                
    def open(self, name):
        createdFileIndex = -1
        for j in range(0,512,8):
            emulatedDisk.seek(self,0,j)
            if emulatedDisk.compareByName2(self, self.OFT[0][0], self.OFT[0][1], name):
                createdFileIndex = emulatedDisk.getIntFromBytes2(self, self.OFT[0][0], self.OFT[0][1]+4)  
                break
        oftIndex = -1
        for i in range(4):
            if self.OFT[i][1] == -1:
                oftIndex = i  
                break    
        if createdFileIndex == -1 or oftIndex == -1:
            return "error"
        fdBlock = (int) (((createdFileIndex * 16) / 512) +1)
        descriptorPos = (int) ((createdFileIndex * 16) % 512)
        fileSize = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos)
        self.OFT[oftIndex][1] = 0
        self.OFT[oftIndex][2] = fileSize
        self.OFT[oftIndex][3] = createdFileIndex
        
        if fileSize == 0:
            pass
        return str(createdFileIndex)
    
    def close(self, oftIndex):
        fileDescriptorIndex = self.OFT[oftIndex][3]
        fdBlock = (int) (((fileDescriptorIndex * 16) / 512) +1)
        descriptorPos = (int) ((fileDescriptorIndex * 16) % 512)
        pos = self.OFT[oftIndex][1]
        b = -1
        if pos < 512 and pos > -1:
            b = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos+4)
        elif pos > 511 and pos < 1024:
            b = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos+8)
        elif pos > 1023 and pos < 1537:
            b = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos+12)
        for i in range(512):
            self.byteArray[b][i] = self.OFT[oftIndex][0][i]
#         self.byteArray[fdBlock][descriptorPos] = self.OFT[oftIndex][3]
        self.OFT[oftIndex][1] = -1
        return True
        
        
    
    def read(self, ind, memoryPos, count):

        fdBlock =(int) (((ind * 16) / 512) +1)
        descriptorPos = ((ind * 16) % 512)
        oftIndex = -1
        b = -1
        for i in range(4):
            if self.OFT[i][3] == ind:
                oftIndex = i
                break
        fileSize  = self.OFT[oftIndex][1]
        bufferPos = fileSize
        
        unfinished = False
        finalBufferPos = 0
        counter = -1
        for i in range(bufferPos,bufferPos+count):
            if i > 511:
                unfinished = True
                break
            counter += 1
            self.M[memoryPos+counter+300] = self.OFT[oftIndex][0][i]
            finalBufferPos = i
        if not unfinished:
            self.OFT[oftIndex][1] = finalBufferPos
            return True
        
#         TODO end of r/w buffer reached
        return True
        
        
        
        
    def write(self, ind, memoryPos, count):
        fdBlock =(int) (((ind * 16) / 512) +1)
        descriptorPos = ((ind * 16) % 512)
        oftIndex = -1
        b = -1
        for i in range(4):
            if self.OFT[i][3] == ind:
                oftIndex = i
                break
        fileSize  = self.OFT[oftIndex][1]
        bufferPos = fileSize % 512
        unfinished = False
        for i in range(bufferPos,bufferPos+count):
            if i > 511:
                unfinished = True
                break
            self.OFT[oftIndex][0][i] = self.M[i]
            finalBufferPos = i
            
            
        if not unfinished:
            if finalBufferPos > fileSize:
                self.OFT[oftIndex][1] = finalBufferPos+1
                
                emulatedDisk.setBytesToInt2(self, self.OFT[0][0], descriptorPos, finalBufferPos)
                emulatedDisk.setBytesToInt(self,self.byteArray,fdBlock,descriptorPos,finalBufferPos)
#                 print(emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos))
#                 print(ind,fdBlock,descriptorPos, )
            return True
        
#         TODO end of r/w buffer reached
        return True
            
        
    
    def seek(self, ind, pos):
        
        fdBlock =(int) (((ind * 16) / 512) +1)
        descriptorPos = ((ind * 16) % 512)
        oftIndex = -1
        b = -1
        for i in range(4):
            if self.OFT[i][3] == ind:
                oftIndex = i
                break
        self.OFT[oftIndex][2] = emulatedDisk.getIntFromBytes(self,self.byteArray,fdBlock,descriptorPos)
        if pos > emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos):
            return False
        if pos < 512 and pos > -1:
            b = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos+4)
        elif pos > 511 and pos < 1024:
            b = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos+8)
        elif pos > 1023 and pos < 1537:
            b = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos+12)
        
#         for i in range(512):
#             self.OFT[oftIndex][0][i] = self.byteArray[b][i]
        self.OFT[oftIndex][1] = pos
    
        
#         print(oftIndex)
        return True
        
        
    
    def directory(self):
        str1 = ""
        for j in range(0,512,8):
            emulatedDisk.seek(self,0,j)
            if emulatedDisk.getIntFromBytes2(self,self.OFT[0][0],self.OFT[0][1]+4) != 0:
                ind = self.getIntFromBytes2(self.OFT[0][0], self.OFT[0][1]+4)
                fdBlock =(int) (((ind * 16) / 512) +1)
                descriptorPos = ((ind * 16) % 512)
                fileSize = emulatedDisk.getIntFromBytes(self, self.byteArray, fdBlock, descriptorPos)
                if (fileSize > 0):
                    fileSize += 1
                
                str1 += self.OFT[0][0][self.OFT[0][1]:self.OFT[0][1]+3].decode('utf-8')
                str1 += " "
                str1 += str(fileSize)
                str1 += " "

        return str1[:-1]
    
    def rm(self, memoryPos, count):
        str = ""
        for i in range(memoryPos, memoryPos+count):
            str += self.M[i:i+1].decode('utf-8')
        return str
    
    def wm(self, memoryPos, inputString):
        arrStringBytes = bytes(inputString, 'utf-8')
        count = -1
        for i in range(memoryPos, len(arrStringBytes)):
            count += 1
            self.M[i] = arrStringBytes[i]
        return count
        
        
    def toString(self):
        for i in range(7,8):
            for j in range(len(self.byteArray[1])):
                print(i,j,self.byteArray[i][j])
        