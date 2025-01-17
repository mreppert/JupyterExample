from IPython.display import display_markdown
from datetime import date
import datetime

class schedule:
    def __init__(self, meetdays, start_date):
        self.events = []
        self.start_date = date.fromisoformat(start_date)
        self.last_date = self.start_date + datetime.timedelta(-1)
        self.holidays = []
        daycodes = 'MTWUFAS'
        self.weekdays = []
        for d in meetdays:
            found_code = False
            for n in range(0, len(daycodes)):
                if daycodes[n]==d:
                    self.weekdays.append(n)
                    found_code = True
            if found_code==False:
                print('Warning: Could not match string \"' + d + '\" to a weekday code')

    def next_free_date(self):
        foundDate = False
        for delta in range(1, 365):
            dt1 = self.last_date + datetime.timedelta(delta)
            
            # First check if class usually meets on this day
            isMeetDay = False
            for m in self.weekdays:
                if dt1.weekday()==m:
                    isMeetDay = True
            
            # If so, check if it's a holiday
            if isMeetDay:
                isHoliday = False
                for hol in self.holidays:
                    # If it is a holiday, add holiday to the list of events
                    if hol[0]==dt1:
                        isHoliday = True
                        holitem = content('holiday', hol[1])
                        holitem.date = hol[0]
                        self.events.append(holitem)
            
            # If it is a valid class day, break out of the loop
            if isMeetDay and (not isHoliday):
                foundDate = True
                break
        if foundDate:
            return dt1
        else:
            return -1
    
    def add_holiday(self, datestring, htitle):
        self.holidays.append([date.fromisoformat(datestring), htitle])
        # If we've already scheduled events LATER than the new holiday
        # we need to re-schedule:
        if self.last_date >= date.fromisoformat(datestring):
            old_event_list = self.events
            self.events = []
            self.last_date = self.start_date + datetime.timedelta(-1)
            for item in old_event_list:
                if item.cformat != 'holiday':
                    self.add_content(item)
                
    def add_content(self, item):
        dt = self.next_free_date()
        item.date = dt
        self.events.append(item)
        self.last_date = item.date
                
    def print_events(self):
        week = 0
        module = 0
        lastday = 8
        mdtext = 'Welcome to Molecular Spectroscopy!\r\rThe schedule below will be updated regularly with links to online materials for each lecture. Dark blue text indicates a Jupyter Notebook-based programming/simulation module, while light-blue headings link to PDF-format lecture notes. Holidays are indicated in purple. Underlining indicates that the link is active and ready for use. A complete list of lecture notes from the most recent year is accessible [here](https://mreppert.github.io/education/chm676f22/notes/index.html). A free PDF copy of the textbook is available for download [here](https://mreppert.github.io/education/chm676f22/textbook.pdf).\r\r**Information on the [Final Project](./git/CHM676/src/CHM676_Final_Project_F2024.pdf) is now posted**.'
        for item in self.events:
            if item.isnew:
                module += 1
                mdtext += "\r"
                mdtext += '## Module ' + str(module) + " \r"
            if item.date.weekday() < lastday:
                week += 1
                mdtext += '#### Week ' + str(week) + "\r"
            lastday = item.date.weekday()
            datetext = " * " + item.date.strftime("%b %-d") + ": "
            
            holiday_color = 'Purple'
            lecture_color = '#3090C7'
            compute_color = 'DarkBlue'
            
            if item.cformat=='holiday':
                titlecol = holiday_color
            elif item.cformat=='lecture':
                titlecol = lecture_color
            elif item.cformat=='compute':
                titlecol = compute_color
            else:
                titletext = item.title
                
            if len(item.link)>0:
                titletext = "<a href=\""+ item.link + "\"> <span style=\"color:" + titlecol + ";text-decoration:underline\">" + item.title + "</span></a>"
            else:
                titletext = "<span style=\"color:" + titlecol + "\">" + item.title + "</span>"
                #titletext = '[' + titletext + '](' + item.link + ')'
            
            if len(item.vlink)>0:
                titletext += ' ([supplement](' + item.vlink + '))'
            
                
            mdtext += datetext + titletext + " \r\r"
        display_markdown(mdtext, raw=True)

class content:
    def __init__(self, cformat, title, newtopic=False, link='', vlink=''):
        self.cformat = cformat
        self.title = title
        self.link = link
        self.vlink = vlink
        self.date = -1
        self.isnew = newtopic


def build_schedule(srcdir):
    schd = schedule('MWF', '2024-08-19')

    schd.add_holiday('2024-09-02', 'Labor Day')
    schd.add_holiday('2024-10-07', 'October Break')
    schd.add_holiday('2024-10-08', 'October Break')
    
    schd.add_holiday('2024-11-27', 'Thanksgiving')
    schd.add_holiday('2024-11-28', 'Thanksgiving')
    schd.add_holiday('2024-11-29', 'Thanksgiving')
    schd.add_holiday('2024-11-30', 'Thanksgiving')

    schd.add_holiday('2024-12-09', 'Finals')
    schd.add_holiday('2024-12-10', 'Finals')
    schd.add_holiday('2024-12-11', 'Finals')
    schd.add_holiday('2024-12-12', 'Finals')
    schd.add_holiday('2024-12-13', 'Finals')
    schd.add_holiday('2024-12-14', 'Finals')

    schd.add_content(content('compute', 'Python Crash Course: Introduction', link=srcdir+'programming/definitions.ipynb', newtopic=True, vlink='https://youtu.be/d9ceCaVjG3o'))
    schd.add_content(content('compute', 'Python Crash Course: Python Arrays', link=srcdir+'programming/arrays.ipynb', vlink='https://youtu.be/oBBv6zHXEKE'))
    schd.add_content(content('compute', 'Python Crash Course: Molecular Dynamics', link=srcdir+'programming/md.ipynb'))

    schd.add_content(content('lecture', 'Maxwell\'s equations and the Lorentz Force Law' , link='https://mreppert.github.io/education/chm676f20/notes/MaxwellsEquations.pdf'))#, vlink='https://youtu.be/bwC38gprBo4'))
    schd.add_content(content('lecture', 'Electromagnetic Waves in Vacuum', link='https://mreppert.github.io/education/chm676f20/notes/VacuumWaves.pdf'))#, vlink='https://purdue.brightspace.com/d2l/home/52483'))
    schd.add_content(content('compute', 'Fourier Transforms', link=srcdir+'FT/FourierTransforms.ipynb'))#, vlink='https://purdue.brightspace.com/d2l/home/52483'))

    schd.add_content(content('lecture', 'Energy Content in EM Waves', link='https://mreppert.github.io/education/chm676f20/notes/EnergyContent.pdf'))#, vlink='https://purdue.brightspace.com/d2l/home/52483'))
    schd.add_content(content('compute', 'MD in an Electric Field', link=srcdir+'MDinEField/MD.ipynb'))

    schd.add_content(content('lecture', 'Microscopic Electrodynamics: The Wave Equation', link='https://mreppert.github.io/education/chm676f20/notes/MicroscopicElectrodynamics.pdf'))#, vlink='https://983291-6.kaf.kaltura.com/media/1_sxgljsx0'))
    schd.add_content(content('lecture', 'Macroscopic Electrodynamics: Ensemble-Averaged Fields', link='https://mreppert.github.io/education/chm676f20/notes/MacroscopicElectrodynamics.pdf'))
    schd.add_content(content('compute', 'Langevin Dynamics', link=srcdir+'Langevin/Langevin.ipynb'))
    schd.add_content(content('compute', 'Material Polarization', link=srcdir+'Langevin/Langevin_oscillators.ipynb'))
#     schd.add_content(content('lecture', 'Review'))
    schd.add_content(content('lecture', 'Practice Exam 1', link=srcdir+'Exam1/exam1_practice.ipynb'))
    schd.add_content(content('lecture', 'Exam (link will be activated at exam time)', link=srcdir+'Exam1/exam1.ipynb'))

    schd.add_content(content('lecture', 'Response Theory', newtopic=True, link='https://mreppert.github.io/education/chm676f20/notes/ResponseTheory.pdf'))
    schd.add_content(content('lecture', 'Linear Response', link='https://mreppert.github.io/education/chm676f20/notes/LinearResponse.pdf'))
    schd.add_content(content('compute', 'Absorption Spectroscopy', link=srcdir+'Langevin/LangevinAbsorption.ipynb'))

    schd.add_content(content('lecture', 'Nonlinear Response', link='https://mreppert.github.io/education/chm676f20/notes/NonlinearResponse.pdf'))
    schd.add_content(content('lecture', 'Nonlinear Spectroscopy', link='https://mreppert.github.io/education/chm676f20/notes/NonlinearSpectroscopy.pdf'))
    schd.add_content(content('compute', 'The Morse Oscillator', link=srcdir+'Morse/exercise6.ipynb'))

    schd.add_content(content('lecture', 'Fluorescence and Hole Burning', link='https://mreppert.github.io/education/chm676f20/notes/FluorescenceHoleBurning.pdf'))
#     schd.add_content(content('compute', 'Convolutions and Hole Burning', link=srcdir+'Broadening/Convolutions.ipynb'))
    schd.add_content(content('compute', 'Broadening Mechanisms and Motional Narrowing', link=srcdir+'Broadening/broadening.ipynb', vlink=srcdir+'Broadening/Convolutions.ipynb'))

    schd.add_content(content('compute', 'Pump-Probe Spectroscopy', link=srcdir+'Morse/PumpProbe.ipynb'))
    schd.add_content(content('lecture', '2D Spectroscopy', link='https://mreppert.github.io/education/chm676f20/notes/PPand2D.pdf'))
    schd.add_content(content('compute', 'Morse Oscillator Nonlinear Spectroscopy', link=srcdir+'Morse/2DSupplement.ipynb'))
#     schd.add_content(content('lecture', 'Review'))#, link='https://mreppert.github.io/education/chm676f20/notes/Module2Review.pdf'))
    schd.add_content(content('lecture', 'Practice Exam2 (F2022)', link=srcdir+'Exam2/exam2f22.ipynb'))
    schd.add_content(content('lecture', 'Practice Exam2', link=srcdir+'Exam2/practice_exam2.ipynb'))
    schd.add_content(content('lecture', 'Exam 2', link=srcdir+'Exam2/exam2f24.ipynb'))
    
    schd.add_content(content('lecture', 'Intro to Quantum Mechanics', newtopic=True, link='https://mreppert.github.io/education/chm676f20/notes/IntroQuantumMechanics.pdf'))
    schd.add_content(content('lecture', 'Linear Alebra Concepts'))
    schd.add_content(content('lecture', 'Quantum Morse Oscillator', link=srcdir+'Quantum/QuantumMorse.ipynb', vlink=srcdir+'Quantum/LinearAlgebra.ipynb'))
    
    schd.add_content(content('lecture', 'Quantum Response Theory I', link='https://mreppert.github.io/education/chm676f20/notes/QuantumResponseTheory.pdf'))
    schd.add_content(content('lecture', 'Quantum Response Theory II', link='https://mreppert.github.io/education/chm676f20/notes/QuantumResponseTheory.pdf'))
    schd.add_content(content('compute', 'Storyline workshopping'))

    schd.add_content(content('lecture', 'Arrow-Ladder Diagrams I', link='https://mreppert.github.io/education/chm676f20/notes/DiagrammaticExpansions.pdf'))
    schd.add_content(content('lecture', 'Arrow-Ladder Diagrams II', link='https://mreppert.github.io/education/chm676f20/notes/DiagrammaticExpansions.pdf'))
    schd.add_content(content('compute', 'Photosynthetic Excitons', link=srcdir+'excitons/PigmentHunter.ipynb'))
    
    schd.add_content(content('lecture', ''))
    
    schd.add_content(content('lecture', ''))
    schd.add_content(content('lecture', ''))
    schd.add_content(content('lecture', 'Project Presentation'))
    
    schd.add_content(content('lecture', 'Project Presentation'))
    schd.add_content(content('lecture', 'Project Presentation'))
    schd.add_content(content('lecture', 'Project Presentation'))

    schd.add_content(content('lecture', 'Freedom!'))
    return schd




