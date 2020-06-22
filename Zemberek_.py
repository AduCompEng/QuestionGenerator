import jpype
import os
from os.path import join
from jpype import JClass, getDefaultJVMPath

class ZemberekInit:

    def __init__(self, libjvmpath=None):
        if libjvmpath is not None:
            self.libjvmpath = getDefaultJVMPath()
        else:
            self.libjvmpath = libjvmpath
        self.zemberekJarpath = os.getcwd() + join('\\', 'bin', 'zemberek-full.jar')

    def zemberek(self):
        try:
            if not jpype.isJVMStarted():
                jpype.startJVM(self.libjvmpath, "-Djava.class.path=" + self.zemberekJarpath, "-ea", convertStrings=False)
                return JClass("zemberek.morphology.TurkishMorphology")
            else:
                # print("Zaten jvm çalışıyor!")
                return JClass("zemberek.morphology.TurkishMorphology")
        except:
            print("Libjvm veya zemberek.jar dosyalarının pathleri yanlış yerde! ")

#ZemberekInit(libjvmpath=r"C:\Program Files\Java\jdk1.8.0_151\jre\bin\server\jvm.dll").zemberek()