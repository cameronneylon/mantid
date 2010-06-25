#
# DO NOT USE THIS SCRIPT FOR RUNNING MANTID. SEE NOTES BELOW!!!!!!!!!!!!!!
#
# This is a test file for the various functions and modules being developed
# for Mantid. In the main Mantid script directory the equivalent of this 
# module is the main entry point into Mantid functionality. Here there are
# just the required methods, many with deeper references removed, and Global 
# variables to enable testing outside of Mantid.
#
#
#


# ---------------------------- CORRECTION INPUT -----------------------------------------
# The information between this line and the other '-----' delimiter needs to be provided
# for the script to function. From the GUI, the tags will be replaced by the appropriate
# information. 

# The tags get replaced by input from the GUI
# The workspaces
SCATTER_SAMPLE = None
SCATTER_CAN = ''
TRANS_SAMPLE = ''
TRANS_CAN = ''
PERIOD_NOS = { "SCATTER_SAMPLE":1, "SCATTER_CAN":1 }
DIRECT_SAMPLE = ''
DIRECT_CAN = ''
DIRECT_CAN = ''
# if the workspaces come from multi-period i.e. group workspaces, the number of periods in that group will be stored in the following variables. These variables corrospond with those above
_SAMPLE_N_PERIODS = -1
_CAN_N_PERIODS =-1
_TRANS_SAMPLE_N_PERIODS = -1
DIRECT_SAMPLE_N_PERIODS = -1
TRANS_SAMPLE_N_CAN = -1
DIRECT_SAMPLE_N_CAN = -1

#This is stored as UserFile in the output workspace
MASKFILE = '_ no file'
# Now the mask string (can be empty)
# These apply to both detectors
SPECMASKSTRING = ''
TIMEMASKSTRING = ''
# These are for the separate detectors (R = main & F = HAB for LOQ)
SPECMASKSTRING_R = ''
SPECMASKSTRING_F = ''
TIMEMASKSTRING_R = ''
TIMEMASKSTRING_F = ''

# Instrument information
# INSTR_DIR = mtd.getConfigProperty('instrumentDefinition.directory')
INSTR_NAME = 'SANS2D'
# Beam centre in metres
XBEAM_CENTRE = None
YBEAM_CENTRE = None

# Analysis tab values
RMIN = None
RMAX = None
DEF_RMIN = None
DEF_RMAX = None
WAV1 = None
WAV2 = None
DWAV = None
Q_REBIN = None
QXY2 = None
DQXY = None
DIRECT_BEAM_FILE_R = None
DIRECT_BEAM_FILE_F = None
GRAVITY = False
# This indicates whether a 1D or a 2D analysis is performed
CORRECTION_TYPE = '1D'
# Component positions
SAMPLE_Z_CORR = 0.0
PHIMIN=-90.0
PHIMAX=90.0
PHIMIRROR=True

# Scaling values
RESCALE = 100.  # percent
SAMPLE_GEOM = 3
SAMPLE_WIDTH = 1.0
SAMPLE_HEIGHT = 1.0
SAMPLE_THICKNESS = 1.0 

# These values are used for the start and end bins for FlatBackground removal.
###############################################################################################
# RICHARD'S NOTE FOR SANS2D: these may need to vary with chopper phase and detector distance !
# !TASK! Put the values in the mask file if they need to be different ?????
##############################################################################################
# The GUI will replace these with default values of
# LOQ: 31000 -> 39000
# S2D: 85000 -> 100000
BACKMON_START = None
BACKMON_END = None

# The detector bank to look at. The GUI has an options box to select the detector to analyse. 
# The spectrum numbers are deduced from the name within the rear-detector tag. Names are from the 
# instrument definition file
# LOQ: HAB or main-detector-bank
# S2D: front-detector or rear-detector 
DETBANK = None

# The monitor spectrum taken from the GUI
MONITORSPECTRUM = 2
# agruments after MON/LENGTH need to take precendence over those after MON/SPECTRUM and this variable ensures that
MONITORSPECLOCKED = False
# if this is set InterpolationRebin will be used on the monitor spectrum used to normalise the sample
SAMP_INTERPOLATE = False

# Detector position information for SANS2D
FRONT_DET_RADIUS = 306.0
FRONT_DET_DEFAULT_SD_M = 4.0
FRONT_DET_DEFAULT_X_M = 1.1
REAR_DET_DEFAULT_SD_M = 4.0

# LOG files for SANS2D will have these encoder readings  
FRONT_DET_Z = 0.0
FRONT_DET_X = 0.0
FRONT_DET_ROT = 0.0
REAR_DET_Z = 0.0
# Rear_Det_X  Will Be Needed To Calc Relative X Translation Of Front Detector 
REAR_DET_X = 0.0

# MASK file stuff ==========================================================
# correction terms to SANS2d encoders - store in MASK file ?
FRONT_DET_Z_CORR = 0.0
FRONT_DET_Y_CORR = 0.0 
FRONT_DET_X_CORR = 0.0 
FRONT_DET_ROT_CORR = 0.0
REAR_DET_Z_CORR = 0.0 
REAR_DET_X_CORR = 0.0

#------------------------------- End of input section -----------------------------------------

# Transmission variables
TRANS_FIT_DEF = 'Log'
TRANS_FIT = TRANS_FIT_DEF
# Map input values to Mantid options
TRANS_FIT_OPTIONS = {
'YLOG' : 'Log',
'STRAIGHT' : 'Linear',
'CLEAR' : 'Off',
# Add Mantid ones as well
'LOG' : 'Log',
'LINEAR' : 'Linear',
'LIN' : 'Linear',
'OFF' : 'Off'
}
TRANS_WAV1 = None
TRANS_WAV2 = None
TRANS_WAV1_FULL = None
TRANS_WAV2_FULL = None
# Mon/Det for SANS2D
TRANS_UDET_MON = 2
TRANS_UDET_DET = 3
# this is if to use InterpolatingRebin on the monitor spectrum used to normalise the transmission
TRANS_INTERPOLATE = False

###################################################################################################################
#
#                              Interface functions (to be called from scripts or the GUI)
#
###################################################################################################################
_NOPRINT_ = False
_VERBOSE_ = False
# "Enumerations"
DefaultTrans = True
NewTrans = False
# Mismatched detectors
_MARKED_DETS_ = []

_DET_ABBREV = {'FRONT' : 'front-detector', 'REAR' : 'rear-detector', 'MAIN' : 'main-detector-bank', 'HAB' : 'HAB' }

def SetNoPrintMode(quiet = True):
    global _NOPRINT_
    _NOPRINT_ = quiet

def SetVerboseMode(state):
    global _VERBOSE_
    _VERBOSE_ = state

# Print a message and log it if the 
def _printMessage(msg, log = True):
    if log == True and _VERBOSE_ == True:
        mantid.sendLogMessage('::SANS::' + msg)
    if _NOPRINT_ == True: 
        return
    print msg

# Warn the user
def _issueWarning(msg):
    mantid.sendLogMessage('::SANS::Warning: ' + msg)
    if _NOPRINT_ == True:
        return
    print 'WARNING: ' + msg

# Fatal error
def _fatalError(msg):
    exit(msg)

DATA_PATH = ''
# Set the data directory
def DataPath(directory):
    _printMessage('DataPath("' + directory + '") - Will look for raw data here')
    if os.path.exists(directory) == False:
        _issueWarning("Data directory does not exist")
        return
    global DATA_PATH
    DATA_PATH = directory

USER_PATH = ''
# Set the user directory
def UserPath(directory):
    _printMessage('UserPath("' + directory + '") - Will look for mask file here')
    if os.path.exists(directory) == False:
        _issueWarning("Data directory does not exist")
        return
    global USER_PATH
    USER_PATH = directory

##################################################### 
# Access function for retrieving parameters
#####################################################
def printParameter(var):
    exec('print ' + var)

########################### 
# Instrument
########################### 
def SANS2D():
    _printMessage('SANS2D()')
    global INSTR_NAME, TRANS_WAV1, TRANS_WAV2, TRANS_WAV1_FULL, TRANS_WAV2_FULL
    INSTR_NAME = 'SANS2D'
    TRANS_WAV1_FULL = TRANS_WAV1 = 2.0
    TRANS_WAV2_FULL = TRANS_WAV2 = 14.0
    if DETBANK != 'rear-detector':
        Detector('rear-detector')

def LOQ():
    _printMessage('LOQ()')
    global INSTR_NAME, MONITORSPECTRUM, TRANS_WAV1, TRANS_WAV2, TRANS_WAV1_FULL, TRANS_WAV2_FULL
    INSTR_NAME = 'LOQ'
    MONITORSPECTRUM = 2
    TRANS_WAV1_FULL = TRANS_WAV1 = 2.2
    TRANS_WAV2_FULL = TRANS_WAV2 = 10.0
    if DETBANK != 'main-detector-bank':
        Detector('main-detector-bank')

def Detector(det_name):
    _printMessage('Detector("' + det_name + '")')
    # Deal with abbreviations
    lname = det_name.lower()
    if lname == 'front':
        det_name = 'front-detector'
    elif lname == 'rear':
        det_name = 'rear-detector'
    elif lname == 'main':
        det_name = 'main-detector-bank'
    elif lname == 'hab':
        det_name = 'HAB'
    else:
        pass
    global DETBANK

    if INSTR_NAME == 'SANS2D' and (det_name == 'rear-detector' or det_name == 'front-detector') or \
       INSTR_NAME == 'LOQ' and (det_name == 'main-detector-bank' or det_name == 'HAB'):
        DETBANK = det_name
    else:
        _issueWarning('Attempting to set invalid detector name "' + det_name + '" for instrument ' + INSTR_NAME)
        if INSTR_NAME == 'LOQ':
            _issueWarning('Setting default as main-detector-bank')
            DETBANK = 'main-detector-bank'
        else:
            _issueWarning('Setting default as rear-detector')
            DETBANK = 'rear-detector'

def Set1D():
    _printMessage('Set1D()')
    global CORRECTION_TYPE
    CORRECTION_TYPE = '1D'

def Set2D():
    _printMessage('Set2D()')
    global CORRECTION_TYPE
    CORRECTION_TYPE = '2D'

########################### 
# Set the scattering sample raw workspace
########################### 
_SAMPLE_SETUP = None
_SAMPLE_RUN = ''
def AssignSample(sample_run, reload = True, period = -1):
    _printMessage('AssignSample("' + sample_run + '")')
    global SCATTER_SAMPLE, _SAMPLE_SETUP, _SAMPLE_RUN, _SAMPLE_N_PERIODS, PERIOD_NOS
    
    __clearPrevious(SCATTER_SAMPLE,others=[SCATTER_CAN,TRANS_SAMPLE,TRANS_CAN,DIRECT_SAMPLE,DIRECT_CAN])
    _SAMPLE_N_PERIODS = -1
    
    if( sample_run.startswith('.') or sample_run == '' or sample_run == None):
        _SAMPLE_SETUP = None
        _SAMPLE_RUN = ''
        SCATTER_SAMPLE = None
        return '', '()'
    
    _SAMPLE_RUN = sample_run
    SCATTER_SAMPLE,reset,logname,filepath, _SAMPLE_N_PERIODS = _assignHelper(sample_run, False, reload, period)
    
    _printMessage('Logname: ' + logname)
    _printMessage('Filepath: ' + filepath)
    if SCATTER_SAMPLE.getName() == '':
        _issueWarning('Unable to load sans sample run, cannot continue.')
        return '','()'
    if reset == True:
        _SAMPLE_SETUP = None
    if (INSTR_NAME == 'SANS2D'):
        global _MARKED_DETS_
        _MARKED_DETS_ = []
        logvalues = _loadDetectorLogs(logname,filepath)
        if logvalues == None:
            mtd.deleteWorkspace(SCATTER_SAMPLE.getName())
            _issueWarning("Sample logs cannot be loaded, cannot continue")
            return '','()'
    else:
        PERIOD_NOS["SCATTER_SAMPLE"] = period
        return SCATTER_SAMPLE.getName(), None
        
    global FRONT_DET_Z, FRONT_DET_X, FRONT_DET_ROT, REAR_DET_Z, REAR_DET_X
    FRONT_DET_Z = float(logvalues['Front_Det_Z'])
    FRONT_DET_X = float(logvalues['Front_Det_X'])
    FRONT_DET_ROT = float(logvalues['Front_Det_Rot'])
    REAR_DET_Z = float(logvalues['Rear_Det_Z'])
    REAR_DET_X = float(logvalues['Rear_Det_X'])

    PERIOD_NOS["SCATTER_SAMPLE"] = period
    return SCATTER_SAMPLE.getName(), logvalues

########################### 
# Set the scattering can raw workspace
########################### 
_CAN_SETUP = None
_CAN_RUN = ''
def AssignCan(can_run, reload = True, period = -1):
    _printMessage('AssignCan("' + can_run + '")')
    global SCATTER_CAN, _CAN_SETUP, _CAN_RUN, _CAN_N_PERIODS, PERIOD_NOS
    
    __clearPrevious(SCATTER_CAN,others=[SCATTER_SAMPLE,TRANS_SAMPLE,TRANS_CAN,DIRECT_SAMPLE,DIRECT_CAN])
    _CAN_N_PERIODS = -1
    
    if( can_run.startswith('.') or can_run == '' or can_run == None):
        SCATTER_CAN.reset()
        _CAN_RUN = ''
        _CAN_SETUP = None
        return '', '()'

    _CAN_RUN = can_run
    SCATTER_CAN ,reset, logname,filepath, _CAN_N_PERIODS = \
        _assignHelper(can_run, False, reload, period)
    if SCATTER_CAN.getName() == '':
        _issueWarning('Unable to load sans can run, cannot continue.')
        return '','()'
    if reset == True:
        _CAN_SETUP  = None
    if (INSTR_NAME == 'SANS2D'):
        global _MARKED_DETS_
        _MARKED_DETS_ = []
        logvalues = _loadDetectorLogs(logname,filepath)
        if logvalues == None:
            _issueWarning("Can logs could not be loaded, using sample values.")
            return SCATTER_CAN.getName(), "()"
    else:
        PERIOD_NOS["SCATTER_CAN"] = period
        return SCATTER_CAN.getName(), ""
    
    smp_values = []
    smp_values.append(FRONT_DET_Z + FRONT_DET_Z_CORR)
    smp_values.append(FRONT_DET_X + FRONT_DET_X_CORR)
    smp_values.append(FRONT_DET_ROT + FRONT_DET_ROT_CORR)
    smp_values.append(REAR_DET_Z + REAR_DET_Z_CORR)
    smp_values.append(REAR_DET_X + REAR_DET_X_CORR)

    PERIOD_NOS["SCATTER_CAN"] = period
    # Check against sample values and warn if they are not the same but still continue reduction
    if len(logvalues) == 0:
        return  SCATTER_CAN.getName(), logvalues
    
    can_values = []
    can_values.append(float(logvalues['Front_Det_Z']) + FRONT_DET_Z_CORR)
    can_values.append(float(logvalues['Front_Det_X']) + FRONT_DET_X_CORR)
    can_values.append(float(logvalues['Front_Det_Rot']) + FRONT_DET_ROT_CORR)
    can_values.append(float(logvalues['Rear_Det_Z']) + REAR_DET_Z_CORR)
    can_values.append(float(logvalues['Rear_Det_X']) + REAR_DET_X_CORR)


    det_names = ['Front_Det_Z', 'Front_Det_X','Front_Det_Rot', 'Rear_Det_Z', 'Rear_Det_X']
    for i in range(0, 5):
        if math.fabs(smp_values[i] - can_values[i]) > 5e-04:
            _issueWarning(det_names[i] + " values differ between sample and can runs. Sample = " + str(smp_values[i]) + \
                              ' , Can = ' + str(can_values[i]))
            _MARKED_DETS_.append(det_names[i])
    
    return SCATTER_CAN.getName(), logvalues

########################### 
# Set the trans sample and measured raw workspaces
########################### 
def TransmissionSample(sample, direct, reload = True, period = -1):
    _printMessage('TransmissionSample("' + sample + '","' + direct + '")')
    global TRANS_SAMPLE, DIRECT_SAMPLE, _TRANS_SAMPLE_N_PERIODS, DIRECT_SAMPLE_N_PERIODS
    
    __clearPrevious(TRANS_SAMPLE,others=[SCATTER_SAMPLE,SCATTER_CAN,TRANS_CAN,DIRECT_SAMPLE,DIRECT_CAN])
    __clearPrevious(DIRECT_SAMPLE,others=[SCATTER_SAMPLE,SCATTER_CAN,TRANS_SAMPLE,TRANS_CAN,DIRECT_CAN])
    
    trans_ws, dummy1, dummy2, dummy3, _TRANS_SAMPLE_N_PERIODS = \
        _assignHelper(sample, True, reload, period)
    TRANS_SAMPLE = trans_ws.getName()
    
    direct_sample_ws, dummy1, dummy2, dummy3, DIRECT_SAMPLE_N_PERIODS = \
        _assignHelper(direct, True, reload, period)
    DIRECT_SAMPLE = direct_sample_ws.getName()
    
    return TRANS_SAMPLE, DIRECT_SAMPLE

########################## 
# Set the trans sample and measured raw workspaces
########################## 
def TransmissionCan(can, direct, reload = True, period = -1):
    _printMessage('TransmissionCan("' + can + '","' + direct + '")')
    global TRANS_CAN, DIRECT_CAN, TRANS_CAN_N_PERIODS, DIRECT_CAN_N_PERIODS
    
    __clearPrevious(TRANS_CAN,others=[SCATTER_SAMPLE,SCATTER_CAN,TRANS_SAMPLE,DIRECT_SAMPLE,DIRECT_CAN])
    __clearPrevious(DIRECT_CAN,others=[SCATTER_SAMPLE,SCATTER_CAN,TRANS_SAMPLE,TRANS_CAN,DIRECT_SAMPLE])

    can_ws, dummy1, dummy2, dummy3, TRANS_CAN_N_PERIODS = \
        _assignHelper(can, True, reload, period)
    TRANS_CAN = can_ws.getName()
    if direct == '' or direct == None:
        DIRECT_CAN, DIRECT_CAN_N_PERIODS = DIRECT_SAMPLE, DIRECT_SAMPLE_N_PERIODS
    else:
        direct_can_ws, dummy1, dummy2, dummy3, DIRECT_CAN_N_PERIODS = \
            _assignHelper(direct, True, reload, period)
        DIRECT_CAN = direct_can_ws.getName()
    return TRANS_CAN, DIRECT_CAN

# Helper function
def _assignHelper(run_string, is_trans, reload = True, period = -1):
    # flag initialised to catch conventional filenames
    flag=None
    if run_string == '' or run_string.startswith('.'):
        return SANSUtility.WorkspaceDetails('', -1),True,'','', -1
    pieces = run_string.split('.')
    if len(pieces) != 2 :
         _fatalError("Invalid run specified: " + run_string + ". Please use RUNNUMBER.EXT format")
    else:
        run_no = pieces[0]
        ext = pieces[1]
    if run_no == '':
        return SANSUtility.WorkspaceDetails('', -1),True,'','', -1
        
    if INSTR_NAME == 'LOQ':
        field_width = 5
    else:
        field_width = 8
        
    fullrun_no,logname,shortrun_no = padRunNumber(run_no, field_width)
    
    if is_trans:
        wkspname =  shortrun_no + '_trans_' + ext.lower()
    else:
        wkspname =  shortrun_no + '_sans_' + ext.lower()

    if reload == False and mtd.workspaceExists(wkspname):
        return WorkspaceDetails(wkspname, shortrun_no),False,'','', -1

    basename = INSTR_NAME + fullrun_no
    filename = os.path.join(DATA_PATH,basename)

    # If a filename that matches the input string exists then assume that is the correct file
    # to load and that a matching log file exists. TODO Check that the log file really does
    # exist.
    if os.path.exists(os.path.join(DATA_PATH, run_string)):
        flag = 1
        filename = os.path.join(DATA_PATH, run_string).rstrip('.nxs')
        _printMessage('_assignHelper: filename: ' + filename)
        logname = run_string.rstrip('.nxs')
        _printMessage('_assignHelper: logname: ' + logname)

    # Workaround so that the FileProperty does the correct searching of data paths if this file doesn't exist
    if not os.path.exists(filename + '.' + ext):
        filename = basename
    if period <= 0:
        period = 1
    if is_trans:
        try:
            if INSTR_NAME == 'SANS2D' and int(shortrun_no) < 568:
                dimension = SANSUtility.GetInstrumentDetails(INSTR_NAME,DETBANK)[0]
                specmin = dimension*dimension*2
                specmax = specmin + 4
            else:
                specmin = None
                specmax = 8
                
            [filepath, wkspname, nPeriods] = \
               _loadRawData(filename, wkspname, ext, specmin, specmax, period)
        except RuntimeError, err:
            _issueWarning(str(err))
            return SANSUtility.WorkspaceDetails('', -1),True,'','', -1
    else:
        try:
            [filepath, wkspname, nPeriods] = _loadRawData(filename, wkspname, ext, None, None, period)
        except RuntimeError, details:
            _issueWarning(str(details))
            return SANSUtility.WorkspaceDetails('', -1),True,'','', -1
            
    inWS = SANSUtility.WorkspaceDetails(wkspname, shortrun_no)
    # If the flag was set above...
    if flag == 1:
        return inWS, True, logname, filepath, nPeriods
    # Otherwise do what was there before
    else:
        return inWS,True, INSTR_NAME + logname, filepath, nPeriods

def padRunNumber(run_no, field_width):
    nchars = len(run_no)
    digit_end = 0
    for i in range(0, nchars):
        if run_no[i].isdigit():
            digit_end += 1
        else:
            break
    
    if digit_end == nchars:
        filebase = run_no.rjust(field_width, '0')
        return filebase, filebase, run_no
    else:
        filebase = run_no[:digit_end].rjust(field_width, '0')
        return filebase + run_no[digit_end:], filebase, run_no[:digit_end]

def __clearPrevious(inWS, others = []):
    if inWS != None:
        if type(inWS) == SANSUtility.WorkspaceDetails:
            inWS = inWS.getName()
        if mtd.workspaceExists(inWS) and (not inWS in others):
            mtd.deleteWorkspace(inWS)

##########################
# Loader function
##########################
def _loadRawData(filename, wsName, ext, spec_min = None, spec_max = None, period=1):
    if ext.lower().startswith('n'):
        alg = LoadNexus(filename + '.' + ext, wsName,SpectrumMin=spec_min,SpectrumMax=spec_max)
    else:
        alg = LoadRaw(filename + '.' + ext, wsName, SpectrumMin = spec_min,SpectrumMax = spec_max)
        LoadSampleDetailsFromRaw(wsName, filename + '.' + ext)

    pWorksp = mtd[wsName]

    if pWorksp.isGroup() :
        #get the number of periods in a group using the fact that each period has a different name
        nNames = len(pWorksp.getNames())
        numPeriods = nNames - 1
    else :
        #if the work space isn't a group there is only one period
        numPeriods = 1
        
    #period greater than one means we must be looking at a workspace group
    if numPeriods > 1 :
        if not pWorksp.isGroup() : raise Exception('_loadRawData: A period number can only be specified for a group and workspace '+ pWorksp.getName() + ' is not a group')
        wsName = _leaveSinglePeriod(pWorksp, period)
        pWorksp = mtd[wsName]
    else :
        #if it is a group but they hadn't specified the period it means load the first spectrum
        if pWorksp.isGroup() :
            wsName = _leaveSinglePeriod(pWorksp, 1)
            pWorksp = mtd[wsName]
    
    sample_details = pWorksp.getSampleDetails()
    SampleGeometry(sample_details.getGeometryFlag())
    SampleThickness(sample_details.getThickness())
    _printMessage('Sample Details: Thick:' + str(sample_details.getThickness())
                  + ' Height:' + str(sample_details.getHeight())
                  + ' Width:' + str(sample_details.getWidth()))
    SampleHeight(sample_details.getHeight())
    SampleWidth(sample_details.getWidth())

    # Return the filepath actually used to load the data
    fullpath = alg.getPropertyValue("Filename")
    return [ os.path.dirname(fullpath), wsName, numPeriods]

def _leaveSinglePeriod(groupW, period):
    #get the name of the individual workspace in the group
    oldName = groupW.getName()+'_'+str(period)
    #move this workspace out of the group (this doesn't delete it)
    groupW.remove(oldName)

    discriptors = groupW.getName().split('_')       #information about the run (run number, if it's 1D or 2D, etc) is listed in the workspace name between '_'s
    for i in range(0, len(discriptors) ):           #insert the period name after the run number
        if i == 0 :                                 #the run number is the first part of the name
            newName = discriptors[0]+'p'+str(period)#so add the period number here
        else :
            newName += '_'+discriptors[i]

    RenameWorkspace(oldName, newName)

    #remove the rest of the group
    mtd.deleteWorkspace(groupW.getName())
    return newName


# Load the detector logs
def _loadDetectorLogs(logname,filepath):
    # Adding runs produces a 1000nnnn or 2000nnnn. For less copying, of log files doctor the filename
    # logname = logname[0:6] + '0' + logname[7:]
    filename = os.path.join(filepath, logname + '.log')
    _issueWarning('I think the log filename is:' + filename)

    # Build a dictionary of log data 
    logvalues = {}
    logvalues['Rear_Det_X'] = '0.0'
    logvalues['Rear_Det_Z'] = '0.0'
    logvalues['Front_Det_X'] = '0.0'
    logvalues['Front_Det_Z'] = '0.0'
    logvalues['Front_Det_Rot'] = '0.0'
    try:
        file_handle = open(filename, 'r')
    except IOError:
        _issueWarning("Log file \"" + filename + "\" could not be loaded.")
        return None
        
    for line in file_handle:
        parts = line.split()
        if len(parts) != 3:
            _issueWarning('Incorrect structure detected in logfile "' + filename + '" for line \n"' + line + '"\nEntry skipped')
        component = parts[1]
        if component in logvalues.keys():
            logvalues[component] = parts[2]
    
    file_handle.close()
    return logvalues

# Return the list of mismatched detector names
def GetMismatchedDetList():
    return _MARKED_DETS_

#########################
# Limits 
def LimitsR(rmin, rmax):
    _printMessage('LimitsR(' + str(rmin) + ',' +str(rmax) + ')')
    _readLimitValues('L/R ' + str(rmin) + ' ' + str(rmax) + ' 1')

def LimitsWav(lmin, lmax, step, type):
    _printMessage('LimitsWav(' + str(lmin) + ',' + str(lmax) + ',' + str(step) + ','  + type + ')')
    _readLimitValues('L/WAV ' + str(lmin) + ' ' + str(lmax) + ' ' + str(step) + '/'  + type)

def LimitsQ(*args):
    # If given one argument it must be a rebin string
    if len(args) == 1:
        val = args[0]
        if type(val) == str:
            _printMessage("LimitsQ(" + val + ")")
            _readLimitValues("L/Q " + val)
        else:
            _issueWarning("LimitsQ can only be called with a single string or 4 values")
    elif len(args) == 4:
        qmin,qmax,step,step_type = args
        _printMessage('LimitsQ(' + str(qmin) + ',' + str(qmax) +',' + str(step) + ',' + str(step_type) + ')')
        _readLimitValues('L/Q ' + str(qmin) + ' ' + str(qmax) + ' ' + str(step) + '/'  + step_type)
    else:
        _issueWarning("LimitsQ called with " + str(len(args)) + " arguments, 1 or 4 expected.")

def LimitsQXY(qmin, qmax, step, type):
    _printMessage('LimitsQXY(' + str(qmin) + ',' + str(qmax) +',' + str(step) + ',' + str(type) + ')')
    _readLimitValues('L/QXY ' + str(qmin) + ' ' + str(qmax) + ' ' + str(step) + '/'  + type)
    
def LimitsPhi(phimin, phimax, use_mirror=True):
    if use_mirror :
        _printMessage("LimitsPHI(" + str(phimin) + ' ' + str(phimax) + 'use_mirror=True)')
        _readLimitValues('L/PHI ' + str(phimin) + ' ' + str(phimax))
    else :
        _printMessage("LimitsPHI(" + str(phimin) + ' ' + str(phimax) + 'use_mirror=False)')
        _readLimitValues('L/PHI/NOMIRROR ' + str(phimin) + ' ' + str(phimax))

def Gravity(flag):
    _printMessage('Gravity(' + str(flag) + ')')
    if isinstance(flag, bool) or isinstance(flag, int):
        global GRAVITY
        GRAVITY = flag
    else:
        _issueWarning("Invalid GRAVITY flag passed, try True/False. Setting kept as " + str(GRAVITY))

def TransFit(mode,lambdamin=None,lambdamax=None):
    global TRANS_WAV1, TRANS_WAV2, TRANS_FIT
    if lambdamin is None or lambdamax is None:
        _printMessage("TransFit(\"" + str(mode) + "\")")
        TRANS_WAV1 = TRANS_WAV1_FULL
        TRANS_WAV2 = TRANS_WAV2_FULL
    else:
        _printMessage("TransFit(\"" + str(mode) + "\"," + str(lambdamin) + "," + str(lambdamax) + ")")
        TRANS_WAV1 = lambdamin
        TRANS_WAV2 = lambdamax

    mode = mode.upper()
    if mode in TRANS_FIT_OPTIONS.keys():
        TRANS_FIT = TRANS_FIT_OPTIONS[mode]
    else:
        _issueWarning("Invalid fit mode passed to TransFit, using default LOG method")
        TRANS_FIT = 'Log'

###################################
# Scaling value
###################################
def _SetScales(scalefactor):
    global RESCALE
    RESCALE = scalefactor * 100.0

######################### 
# Sample geometry flag
######################### 
def SampleGeometry(geom_id):
    if geom_id > 3 or geom_id < 1:
        _issueWarning("Invalid geometry type for sample: " + str(geom_id) + ". Setting default to 3.")
        geom_id = 3
    global SAMPLE_GEOM
    SAMPLE_GEOM = geom_id

######################### 
# Sample width
######################### 
def SampleWidth(width):
    if SAMPLE_GEOM == None:
        _fatalError('Attempting to set width without setting geometry flag. Please set geometry type first')
    global SAMPLE_WIDTH
    SAMPLE_WIDTH = width
    # For a disk the height=width
    if SAMPLE_GEOM == 3:
        global SAMPLE_HEIGHT
        SAMPLE_HEIGHT = width

######################### 
# Sample height
######################### 
def SampleHeight(height):
    if SAMPLE_GEOM == None:
        _fatalError('Attempting to set height without setting geometry flag. Please set geometry type first')
    global SAMPLE_HEIGHT
    SAMPLE_HEIGHT = height
    # For a disk the height=width
    if SAMPLE_GEOM == 3:
        global SAMPLE_WIDTH
        SAMPLE_WIDTH = height

######################### 
# Sample thickness
#########################
def SampleThickness(thickness):
    global SAMPLE_THICKNESS
    SAMPLE_THICKNESS = thickness

#############################
# Print sample geometry
###########################
def displayGeometry():
    print 'Beam centre: [' + str(XBEAM_CENTRE) + ',' + str(YBEAM_CENTRE) + ']'
    print '-- Sample Geometry --\n' + \
        '    ID: ' + str(SAMPLE_GEOM) + '\n' + \
        '    Width: ' + str(SAMPLE_WIDTH) + '\n' + \
        '    Height: ' + str(SAMPLE_HEIGHT) + '\n' + \
        '    Thickness: ' + str(SAMPLE_THICKNESS) + '\n'


######################################
# Set the centre in mm
####################################
def SetCentre(XVAL, YVAL):
    _printMessage('SetCentre(' + str(XVAL) + ',' + str(YVAL) + ')')
    global XBEAM_CENTRE, YBEAM_CENTRE
    XBEAM_CENTRE = XVAL/1000.
    YBEAM_CENTRE = YVAL/1000.

#####################################
# Set the phi limit
#####################################
def SetPhiLimit(phimin,phimax, phimirror=True):
    if phimirror :
        if phimin > phimax:
            phimin, phimax = phimax, phimin
        if abs(phimin) > 180.0 :
            phimin = -90.0
        if abs(phimax) > 180.0 :
            phimax = 90.0
	
        if phimax - phimin == 180.0 :
            phimin = -90.0
            phimax = 90.0
        else:
            phimin = SANSUtility.normalizePhi(phimin)
            phimax = SANSUtility.normalizePhi(phimax)
          
  	
    global PHIMIN, PHIMAX, PHIMIRROR
    PHIMIN = phimin
    PHIMAX = phimax
    PHIMIRROR = phimirror
    

#####################################
# Clear current mask defaults
#####################################
def clearCurrentMaskDefaults():

    Mask('MASK/CLEAR')
    Mask('MASK/CLEAR/TIME')
    SetRearEfficiencyFile(None)
    SetFrontEfficiencyFile(None)
    global RMIN,RMAX, DEF_RMIN, DEF_RMAX
    RMIN = RMAX = DEF_RMIN = DEF_RMAX = None
    global WAV1, WAV2, DWAV, Q_REBIN, QXY2, DQY
    WAV1 = WAV2 = DWAV = Q_REBIN = QXY = DQY = None
    global SAMPLE_Z_CORR
    SAMPLE_Z_CORR = 0.0
    global RESCALE, SAMPLE_GEOM, SAMPLE_WIDTH, SAMPLE_HEIGHT, SAMPLE_THICKNESS
    # Scaling values
    RESCALE = 100.  # percent
    SAMPLE_GEOM = 3
    SAMPLE_WIDTH = SAMPLE_HEIGHT = SAMPLE_THICKNESS = 1.0
    global FRONT_DET_Z_CORR, FRONT_DET_Y_CORR, FRONT_DET_X_CORR, FRONT_DET_ROT_CORR 
    FRONT_DET_Z_CORR = FRONT_DET_Y_CORR = FRONT_DET_X_CORR = FRONT_DET_ROT_CORR = 0.0
    global REAR_DET_Z_CORR, REAR_DET_X_CORR
    REAR_DET_Z_CORR = REAR_DET_X_CORR = 0.0
    
    global BACKMON_START, BACKMON_END
    BACKMON_START = BACKMON_END = None
    
    global MONITORSPECTRUM, MONITORSPECLOCKED, SAMP_INTERPOLATE, TRANS_UDET_MON, TRANS_UDET_DET, TRANS_INTERPOLATE
    MONITORSPECTRUM = 2
    MONITORSPECLOCKED = False
    SAMP_INTERPOLATE = False
    
    TRANS_UDET_MON = 2
    TRANS_UDET_DET = 3
    TRANS_INTERPOLATE = False

####################################
# Add a mask to the correct string
###################################
def Mask(details):
    _printMessage('Mask("' + details + '")')
    details = details.lstrip()
    details_compare = details.upper()
    if not details_compare.startswith('MASK'):
        _issueWarning('Ignoring malformed mask line ' + details)
        return

    global TIMEMASKSTRING, TIMEMASKSTRING_R, TIMEMASKSTRING_F,SPECMASKSTRING, SPECMASKSTRING_R, SPECMASKSTRING_F
    parts = details_compare.split('/')
    # A spectrum mask or mask range applied to both detectors
    if len(parts) == 1:
        spectra = details[4:].lstrip()
        if len(spectra.split()) == 1:
            SPECMASKSTRING += ',' + spectra
    elif len(parts) == 2:
        type = parts[1]
        detname = type.split()
        if type == 'CLEAR':
            SPECMASKSTRING = ''
            SPECMASKSTRING_R = ''
            SPECMASKSTRING_F = ''
        elif type.startswith('T'):
            if type.startswith('TIME'):
                bin_range = type[4:].lstrip()
            else:
                bin_range = type[1:].lstrip()
            TIMEMASKSTRING += ';' + bin_range
        elif len(detname) == 2:
            type = detname[0]
            if type in _DET_ABBREV.keys():
                spectra = detname[1]
                if type == 'FRONT' or type == 'HAB':
                    SPECMASKSTRING_F += ',' + spectra
                else:
                    SPECMASKSTRING_R += ',' + spectra
            else:
                _issueWarning('Unrecognized detector on mask line "' + details + '". Skipping line.')
        else:
            _issueWarning('Unrecognized masking option "' + details + '"')
    elif len(parts) == 3:
        type = parts[1]
        if type == 'CLEAR':
            TIMEMASKSTRING = ''
            TIMEMASKSTRING_R = ''
            TIMEMASKSTRING_F = ''
        elif (type == 'TIME' or type == 'T'):
            parts = parts[2].split()
            if len(parts) == 3:
                detname = parts[0].rstrip()
                bin_range = parts[1].rstrip() + ' ' + parts[2].lstrip() 
                if detname in _DET_ABBREV.keys():
                    if detname == 'FRONT' or detname == 'HAB':
                        TIMEMASKSTRING_F += ';' + bin_range
                    else:
                        TIMEMASKSTRING_R += ';' + bin_range
                else:
                    _issueWarning('Unrecognized detector on mask line "' + details + '". Skipping line.')
            else:
                _issueWarning('Unrecognized masking option "' + details + '"')
    else:
        pass

#############################
# Read a mask file
#############################
def MaskFile(filename):
    _printMessage('MaskFile("' + filename + '")')
    if os.path.isabs(filename) == False:
        filename = os.path.join(USER_PATH, filename)

    if os.path.exists(filename) == False:
        _fatalError("Cannot read mask file '" + filename + "', path does not exist.")
        
    clearCurrentMaskDefaults()

    file_handle = open(filename, 'r')
    for line in file_handle:
        if line.startswith('!'):
            continue
        # This is so that I can be sure all EOL characters have been removed
        line = line.lstrip().rstrip()
        upper_line = line.upper()
        if upper_line.startswith('L/'):
            _readLimitValues(line)
        
        elif upper_line.startswith('MON/'):
            _readMONValues(line)
        
        elif upper_line.startswith('MASK'):
            Mask(upper_line)
        
        elif upper_line.startswith('SET CENTRE'):
            values = upper_line.split()
            SetCentre(float(values[2]), float(values[3]))
        
        elif upper_line.startswith('SET SCALES'):
            values = upper_line.split()
            _SetScales(float(values[2]))
        
        elif upper_line.startswith('SAMPLE/OFFSET'):
            values = upper_line.split()
            SetSampleOffset(values[1])
        
        elif upper_line.startswith('DET/'):
            type = upper_line[4:]
            if type.startswith('CORR'):
                _readDetectorCorrections(upper_line[8:])
            else:
                # This checks whether the type is correct and issues warnings if it is not
                Detector(type)
        
        elif upper_line.startswith('GRAVITY'):
            flag = upper_line[8:]
            if flag == 'ON':
                Gravity(True)
            elif flag == 'OFF':
                Gravity(False)
            else:
                _issueWarning("Gravity flag incorrectly specified, disabling gravity correction")
                Gravity(False)
        
        elif upper_line.startswith('BACK/MON/TIMES'):
            tokens = upper_line.split()
            global BACKMON_START, BACKMON_END
            if len(tokens) == 3:
                BACKMON_START = int(tokens[1])
                BACKMON_END = int(tokens[2])
            else:
                _issueWarning('Incorrectly formatted BACK/MON/TIMES line, not running FlatBackground.')
                BACKMON_START = None
                BACKMON_END = None
        
        elif upper_line.startswith("FIT/TRANS/"):
            params = upper_line[10:].split()
            if len(params) == 3:
                fit_type, lambdamin, lambdamax = params
                TransFit(fit_type, lambdamin, lambdamax)
            else:
                _issueWarning('Incorrectly formatted FIT/TRANS line, setting defaults to LOG and full range')
                TransFit(TRANS_FIT_DEF)
        
        else:
            continue

    # Close the handle
    file_handle.close()
    # Check if one of the efficency files hasn't been set and assume the other is to be used
    if DIRECT_BEAM_FILE_R == None and DIRECT_BEAM_FILE_F != None:
        SetRearEfficiencyFile(DIRECT_BEAM_FILE_F)
    if DIRECT_BEAM_FILE_F == None and DIRECT_BEAM_FILE_R != None:
        SetFrontEfficiencyFile(DIRECT_BEAM_FILE_R)
        
    # just print thhe name, remove the path
    filename = os.path.basename(filename)
    global MASKFILE
    MASKFILE = filename

# Read a limit line of a mask file
def _readLimitValues(limit_line):
    limits = limit_line.split('L/')
    if len(limits) != 2:
        _issueWarning("Incorrectly formatted limit line ignored \"" + limit_line + "\"")
        return
    limits = limits[1]
    limit_type = ''
    if not ',' in limit_line:
        # Split with no arguments defaults to any whitespace character and in particular
        # multiple spaces are include
        elements = limits.split()
        if len(elements) == 4:
            limit_type, minval, maxval, step = elements[0], elements[1], elements[2], elements[3]
            rebin_str = None
            step_details = step.split('/')
            if len(step_details) == 2:
                step_size = step_details[0]
                step_type = step_details[1]
                if step_type.upper() == 'LIN':
                    step_type = ''
                else:
                    step_type = '-'
            else:
                step_size = step_details[0]
                step_type = ''
        elif len(elements) == 3:
            limit_type, minval, maxval = elements[0], elements[1], elements[2]
        else:
            # We don't use the L/SP line
            if not 'L/SP' in limit_line:
                _issueWarning("Incorrectly formatted limit line ignored \"" + limit_line + "\"")
                return
    else:
        limit_type = limits[0].lstrip().rstrip()
        rebin_str = limits[1:].lstrip().rstrip()
        minval = maxval = step_type = step_size = None

    if limit_type.upper() == 'WAV':
        global WAV1, WAV2, DWAV
        WAV1 = float(minval)
        WAV2 = float(maxval)
        DWAV = float(step_type + step_size)
    elif limit_type.upper() == 'Q':
        global Q_REBIN
        if not rebin_str is None:
            Q_REBIN = rebin_str
        else:
            Q_REBIN = minval + "," + step_type + step_size + "," + maxval
    elif limit_type.upper() == 'QXY':
        global QXY2, DQXY
        QXY2 = float(maxval)
        DQXY = float(step_type + step_size)
    elif limit_type.upper() == 'R':
        global RMIN, RMAX, DEF_RMIN, DEF_RMAX
        RMIN = float(minval)/1000.
        RMAX = float(maxval)/1000.
        DEF_RMIN = RMIN
        DEF_RMAX = RMAX
    elif limit_type.upper() == 'PHI':
        SetPhiLimit(float(minval), float(maxval), True)
    elif limit_type.upper() == 'PHI/NOMIRROR':
        SetPhiLimit(float(minval), float(maxval), False)
    else:
        pass

def _readMONValues(line):
    details = line[4:].upper()

    #MON/LENTH, MON/SPECTRUM and MON/TRANS all accept the INTERPOLATE option
    interpolate = False
    if details.endswith('/INTERPOLATE') :
        interpolate = True
        details = details.split('/INTERPOLATE')[0]

    if details.startswith('LENGTH'):
        SuggestMonitorSpectrum(int(details.split()[1]), interpolate)
    
    elif details.startswith('SPECTRUM'):
        SetMonitorSpectrum(int(details.split('=')[1]), interpolate)
    
    elif details.startswith('TRANS'):
        parts = details.split('=')
        if len(parts) < 2 or parts[0] != 'TRANS/SPECTRUM' :
            _issueWarning('Unable to parse MON/TRANS line, needs MON/TRANS/SPECTRUM=')
        SetTransSpectrum(int(parts[1]), interpolate)

    elif 'DIRECT' in details:
        parts = details.split("=")
        if len(parts) == 2:
            filepath = parts[1].rstrip()
            if '[' in filepath:
                idx = filepath.rfind(']')
                filepath = filepath[idx + 1:]
            if not os.path.isabs(filepath):
                filepath = os.path.join(USER_PATH, filepath)
            type = parts[0]
            parts = type.split("/")
            if len(parts) == 1:
                if parts[0] == 'DIRECT':
                    SetRearEfficiencyFile(filepath)
                    SetFrontEfficiencyFile(filepath)
                elif parts[0] == 'HAB':
                    SetFrontEfficiencyFile(filepath)
                else:
                    pass
            elif len(parts) == 2:
                detname = parts[1]
                if detname == 'REAR':
                    SetRearEfficiencyFile(filepath)
                elif detname == 'FRONT' or detname == 'HAB':
                    SetFrontEfficiencyFile(filepath)
                else:
                    _issueWarning('Incorrect detector specified for efficiency file "' + line + '"')
            else:
                _issueWarning('Unable to parse monitor line "' + line + '"')
        else:
            _issueWarning('Unable to parse monitor line "' + line + '"')

def _readDetectorCorrections(details):
    values = details.split()
    det_name = values[0]
    det_axis = values[1]
    shift = float(values[2])

    if det_name == 'REAR':
        if det_axis == 'X':
            global REAR_DET_X_CORR
            REAR_DET_X_CORR = shift
        elif det_axis == 'Z':
            global REAR_DET_Z_CORR
            REAR_DET_Z_CORR = shift
        else:
            pass
    else:
        if det_axis == 'X':
            global FRONT_DET_X_CORR
            FRONT_DET_X_CORR = shift
        elif det_axis == 'Y':
            global FRONT_DET_Y_CORR
            FRONT_DET_Y_CORR = shift
        elif det_axis == 'Z':
            global FRONT_DET_Z_CORR
            FRONT_DET_Z_CORR = shift
        elif det_axis == 'ROT':
            global FRONT_DET_ROT_CORR
            FRONT_DET_ROT_CORR = shift
        else:
            pass    

def SetSampleOffset(value):
    global SAMPLE_Z_CORR
    SAMPLE_Z_CORR = float(value)/1000.

def SetMonitorSpectrum(specNum, interp=False):
    global MONITORSPECTRUM
    MONITORSPECTRUM = int(specNum)
    
    global SAMP_INTERPOLATE
    SAMP_INTERPOLATE = bool(interp)

    global MONITORSPECLOCKED
    MONITORSPECLOCKED = True

def SuggestMonitorSpectrum(specNum, interp=False):
    global MONITORSPECLOCKED
    if MONITORSPECLOCKED :
        return

    global SAMP_INTERPOLATE
    SAMP_INTERPOLATE = bool(interp)
        
    global MONITORSPECTRUM
    MONITORSPECTRUM = int(specNum)

def SetTransSpectrum(specNum, interp=False):
    global TRANS_UDET_MON
    TRANS_UDET_MON = int(specNum)

    global TRANS_INTERPOLATE
    TRANS_INTERPOLATE = bool(interp)

def SetRearEfficiencyFile(filename):
    global DIRECT_BEAM_FILE_R
    DIRECT_BEAM_FILE_R = filename
    
def SetFrontEfficiencyFile(filename):
    global DIRECT_BEAM_FILE_F
    DIRECT_BEAM_FILE_F = filename

def displayMaskFile():
    print '-- Mask file defaults --'
    print '    Wavelength range: ',WAV1, WAV2, DWAV
    print '    Q range: ', Q_REBIN
    print '    QXY range: ', QXY2, DQXY
    print '    radius', RMIN, RMAX
    print '    direct beam file rear:', DIRECT_BEAM_FILE_R
    print '    direct beam file front:', DIRECT_BEAM_FILE_F
    print '    global spectrum mask: ', SPECMASKSTRING
    print '    rear spectrum mask: ', SPECMASKSTRING_R
    print '    front spectrum mask: ', SPECMASKSTRING_F
    print '    global time mask: ', TIMEMASKSTRING
    print '    rear time mask: ', TIMEMASKSTRING_R
    print '    front time mask: ', TIMEMASKSTRING_F

# ---------------------------------------------------------------------------------------

##
# Set up the sample and can detectors and calculate the transmission if available
##
def _initReduction(xcentre = None, ycentre = None):
    # *** Sample setup first ***
    if SCATTER_SAMPLE == None:
        exit('Error: No sample run has been set')

    if xcentre == None or ycentre == None:
        xcentre = XBEAM_CENTRE
        ycentre = YBEAM_CENTRE

    global _SAMPLE_SETUP	
    if _SAMPLE_SETUP == None:
        _SAMPLE_SETUP = _init_run(SCATTER_SAMPLE, [xcentre, ycentre], False)
    
    global _CAN_SETUP
    if SCATTER_CAN.getName() != '' and _CAN_SETUP == None:
        _CAN_SETUP = _init_run(SCATTER_CAN, [xcentre, ycentre], True)

    # Instrument specific information using function in utility file
    global DIMENSION, SPECMIN, SPECMAX
    DIMENSION, SPECMIN, SPECMAX  = SANSUtility.GetInstrumentDetails(INSTR_NAME, DETBANK)

    return _SAMPLE_SETUP, _CAN_SETUP

##
# Run the reduction for a given wavelength range
##
def WavRangeReduction(wav_start = None, wav_end = None, use_def_trans = DefaultTrans, finding_centre = False):
    if wav_start == None:
        wav_start = WAV1
    if wav_end == None:
        wav_end = WAV2

    if finding_centre == False:
        _printMessage('WavRangeReduction(' + str(wav_start) + ',' + str(wav_end) + ',' + str(use_def_trans) + ',' + str(finding_centre) + ')')
        _printMessage("Running reduction for wavelength range " + str(wav_start) + '-' + str(wav_end))
    # This only performs the init if it needs to
    sample_setup, can_setup = _initReduction(XBEAM_CENTRE, YBEAM_CENTRE)

    wsname_cache = sample_setup.getReducedWorkspace()
    # Run correction function
    if finding_centre == True:
        final_workspace = wsname_cache.split('_')[0] + '_quadrants'
    else:
        final_workspace = wsname_cache + '_' + str(wav_start) + '_' + str(wav_end)
    sample_setup.setReducedWorkspace(final_workspace)
    # Perform correction
    Correct(sample_setup, wav_start, wav_end, use_def_trans, finding_centre)

    if can_setup != None:
        tmp_smp = final_workspace+"_sam_tmp"
        RenameWorkspace(final_workspace, tmp_smp)
        # Run correction function
        # was  Correct(SCATTER_CAN, can_setup[0], can_setup[1], wav_start, wav_end, can_setup[2], can_setup[3], finding_centre)
        tmp_can = final_workspace+"_can_tmp"
        can_setup.setReducedWorkspace(tmp_can)
        # Can correction
        Correct(can_setup, wav_start, wav_end, use_def_trans, finding_centre)
        Minus(tmp_smp, tmp_can, final_workspace)

        # Due to rounding errors, small shifts in detector encoders and poor stats in highest Q bins need "minus" the
        # workspaces before removing nan & trailing zeros thus, beware,  _sc,  _sam_tmp and _can_tmp may NOT have same Q bins
        if finding_centre == False:
            ReplaceSpecialValues(InputWorkspace = tmp_smp,OutputWorkspace = tmp_smp, NaNValue="0", InfinityValue="0")
            ReplaceSpecialValues(InputWorkspace = tmp_can,OutputWorkspace = tmp_can, NaNValue="0", InfinityValue="0")
            if CORRECTION_TYPE == '1D':
                SANSUtility.StripEndZeroes(tmp_smp)
                SANSUtility.StripEndZeroes(tmp_can)
        else:
            mantid.deleteWorkspace(tmp_smp)
            mantid.deleteWorkspace(tmp_can)
            mantid.deleteWorkspace(final_workspace)
                
    # Crop Workspace to remove leading and trailing zeroes
    if finding_centre == False:
        # Replaces NANs with zeroes
        ReplaceSpecialValues(InputWorkspace = final_workspace, OutputWorkspace = final_workspace, NaNValue="0", InfinityValue="0")
        if CORRECTION_TYPE == '1D':
            SANSUtility.StripEndZeroes(final_workspace)
        # Store the mask file within the final workspace so that it is saved to the CanSAS file
        AddSampleLog(final_workspace, "UserFile", MASKFILE)
    else:
        quadrants = {1:'Left', 2:'Right', 3:'Up',4:'Down'}
        for key, value in quadrants.iteritems():
            old_name = final_workspace + '_' + str(key)
            RenameWorkspace(old_name, value)
            AddSampleLog(value, "UserFile", MASKFILE)

    # Revert the name change so that future calls with different wavelengths get the correct name
    sample_setup.setReducedWorkspace(wsname_cache)
    return final_workspace

##
# Init helper
##
def _init_run(raw_ws, beamcoords, emptycell):
    if raw_ws == '':
        return None

    if emptycell:
        _printMessage('Initializing can workspace to [' + str(beamcoords[0]) + ',' + str(beamcoords[1]) + ']' )
    else:
        _printMessage('Initializing sample workspace to [' + str(beamcoords[0]) + ',' + str(beamcoords[1]) + ']' )

    if emptycell == True:
        final_ws = "can_temp_workspace"
    else:
        final_ws = raw_ws.getName().split('_')[0]
        if DETBANK == 'front-detector':
            final_ws += 'front'
        elif DETBANK == 'rear-detector':
            final_ws += 'rear'
        elif DETBANK == 'main-detector-bank':
            final_ws += 'main'
        else:
            final_ws += 'HAB'
        final_ws += '_' + CORRECTION_TYPE

    # Put the components in the correct positions
    maskpt_rmin, maskpt_rmax = SetupComponentPositions(DETBANK, raw_ws.getName(), beamcoords[0], beamcoords[1])
    
    # Create a run details object
    if emptycell == True:
        return SANSUtility.RunDetails(raw_ws, final_ws, TRANS_CAN, DIRECT_CAN, maskpt_rmin, maskpt_rmax, 'can')
    else:
        return SANSUtility.RunDetails(raw_ws, final_ws, TRANS_SAMPLE, DIRECT_SAMPLE, maskpt_rmin, maskpt_rmax, 'sample')

##
# Setup the transmission workspace
##
def CalculateTransmissionCorrection(run_setup, lambdamin, lambdamax, use_def_trans):
    trans_raw = run_setup.getTransRaw()
    direct_raw = run_setup.getDirectRaw()
    if trans_raw == '' or direct_raw == '':
        return None

    if use_def_trans == DefaultTrans:
        wavbin = str(TRANS_WAV1_FULL) + ',' + str(DWAV) + ',' + str(TRANS_WAV2_FULL)
        translambda_min = TRANS_WAV1_FULL
        translambda_max = TRANS_WAV2_FULL
    else:
        translambda_min = TRANS_WAV1
        translambda_max = TRANS_WAV2
        wavbin = str(lambdamin) + ',' + str(DWAV) + ',' + str(lambdamax)

    fittedtransws = trans_raw.split('_')[0] + '_trans_' + run_setup.getSuffix() + '_' + str(translambda_min) + '_' + str(translambda_max)
    unfittedtransws = fittedtransws + "_unfitted"
    if use_def_trans == False or \
    (TRANS_FIT != 'Off' and mtd.workspaceExists(fittedtransws) == False) or \
    (TRANS_FIT == 'Off' and mtd.workspaceExists(unfittedtransws) == False):
        # If no fitting is required just use linear and get unfitted data from CalculateTransmission algorithm
        if TRANS_FIT == 'Off':
            fit_type = 'Linear'
        else:
            fit_type = TRANS_FIT
        #retrieve the user setting that tells us whether Rebin or InterpolatingRebin will be used during the normalisation 
        global TRANS_INTERPOLATE
        if INSTR_NAME == 'LOQ':
            # Change the instrument definition to the correct one in the LOQ case
            LoadInstrument(trans_raw, INSTR_DIR + "/LOQ_trans_Definition.xml")
            LoadInstrument(direct_raw, INSTR_DIR + "/LOQ_trans_Definition.xml")
            trans_tmp_out = SANSUtility.SetupTransmissionWorkspace(trans_raw, '1,2', BACKMON_START, BACKMON_END, wavbin, TRANS_INTERPOLATE, True)
            direct_tmp_out = SANSUtility.SetupTransmissionWorkspace(direct_raw, '1,2', BACKMON_START, BACKMON_END, wavbin, TRANS_INTERPOLATE, True)
            CalculateTransmission(trans_tmp_out,direct_tmp_out, fittedtransws, MinWavelength = translambda_min, MaxWavelength =  translambda_max, \
                                  FitMethod = fit_type, OutputUnfittedData=True)
        else:
            trans_tmp_out = SANSUtility.SetupTransmissionWorkspace(trans_raw, '1,2', BACKMON_START, BACKMON_END, wavbin, TRANS_INTERPOLATE, False)
            direct_tmp_out = SANSUtility.SetupTransmissionWorkspace(direct_raw, '1,2', BACKMON_START, BACKMON_END, wavbin, TRANS_INTERPOLATE, False)
            CalculateTransmission(trans_tmp_out,direct_tmp_out, fittedtransws, TRANS_UDET_MON, TRANS_UDET_DET, MinWavelength = translambda_min, \
                                  MaxWavelength = translambda_max, FitMethod = fit_type, OutputUnfittedData=True)
        # Remove temporaries
        mantid.deleteWorkspace(trans_tmp_out)
        mantid.deleteWorkspace(direct_tmp_out)
        
    if TRANS_FIT == 'Off':
        result = unfittedtransws
        mantid.deleteWorkspace(fittedtransws)
    else:
        result = fittedtransws

    if use_def_trans == DefaultTrans:
        tmp_ws = 'trans_' + run_setup.getSuffix() + '_' + str(lambdamin) + '_' + str(lambdamax)
        CropWorkspace(result, tmp_ws, XMin = str(lambdamin), XMax = str(lambdamax))
        return tmp_ws
    else: 
        return result

##
# Setup component positions, xbeam and ybeam in metres
##
def SetupComponentPositions(detector, dataws, xbeam, ybeam):
    # Put the components in the correct place
    # The sample holder
    MoveInstrumentComponent(dataws, 'some-sample-holder', Z = SAMPLE_Z_CORR, RelativePosition="1")
    
    # The detector
    if INSTR_NAME == 'LOQ':
        xshift = (317.5/1000.) - xbeam
        yshift = (317.5/1000.) - ybeam
        MoveInstrumentComponent(dataws, detector, X = xshift, Y = yshift, RelativePosition="1")
        # LOQ instrument description has detector at 0.0, 0.0
        return [xshift, yshift], [xshift, yshift] 
    else:
        if detector == 'front-detector':
            rotateDet = (-FRONT_DET_ROT - FRONT_DET_ROT_CORR)
            RotateInstrumentComponent(dataws, detector,X="0.",Y="1.0",Z="0.",Angle=rotateDet)
            RotRadians = math.pi*(FRONT_DET_ROT + FRONT_DET_ROT_CORR)/180.
            xshift = (REAR_DET_X + REAR_DET_X_CORR - FRONT_DET_X - FRONT_DET_X_CORR + FRONT_DET_RADIUS*math.sin(RotRadians ) )/1000. - FRONT_DET_DEFAULT_X_M - xbeam
            yshift = (FRONT_DET_Y_CORR /1000.  - ybeam)
            # default in instrument description is 23.281m - 4.000m from sample at 19,281m !
            # need to add ~58mm to det1 to get to centre of detector, before it is rotated.
            zshift = (FRONT_DET_Z + FRONT_DET_Z_CORR + FRONT_DET_RADIUS*(1 - math.cos(RotRadians)) )/1000. - FRONT_DET_DEFAULT_SD_M
            MoveInstrumentComponent(dataws, detector, X = xshift, Y = yshift, Z = zshift, RelativePosition="1")
            return [0.0, 0.0], [0.0, 0.0]
        else:
            xshift = -xbeam
            yshift = -ybeam
            zshift = (REAR_DET_Z + REAR_DET_Z_CORR)/1000. - REAR_DET_DEFAULT_SD_M
            mantid.sendLogMessage("::SANS:: Setup move "+str(xshift*1000.)+" "+str(yshift*1000.))
            MoveInstrumentComponent(dataws, detector, X = xshift, Y = yshift, Z = zshift, RelativePosition="1")
            return [0.0,0.0], [xshift, yshift]

        
#----------------------------------------------------------------------------------------------------------------------------
##
# Main correction routine
##
def Correct(run_setup, wav_start, wav_end, use_def_trans, finding_centre = False):
    '''Performs the data reduction steps'''
    global SPECMIN, SPECMAX, MONITORSPECTRUM
    sample_raw = run_setup.getRawWorkspace()
#but does the full run still exist at this point, doesn't matter  I'm changing the meaning of RawWorkspace get all references to it
#but then what do we call the workspaces?

#    period = run_setup.getPeriod()
    orientation = orientation=SANSUtility.Orientation.Horizontal
    if INSTR_NAME == "SANS2D":
        base_runno = sample_raw.getRunNumber()
        if base_runno < 568:
            MONITORSPECTRUM = 73730
            orientation=SANSUtility.Orientation.Vertical
            if DETBANK == 'front-detector':
                SPECMIN = DIMENSION*DIMENSION + 1 
                SPECMAX = DIMENSION*DIMENSION*2
            else:
                SPECMIN = 1
                SPECMAX = DIMENSION*DIMENSION
        elif (base_runno >= 568 and base_runno < 684):
            orientation = SANSUtility.Orientation.Rotated
        else:
            pass

    ############################# Setup workspaces ######################################
    monitorWS = "Monitor"
    _printMessage('monitor ' + str(MONITORSPECTRUM), True)
    sample_name = sample_raw.getName()
    # Get the monitor ( StartWorkspaceIndex is off by one with cropworkspace)
    CropWorkspace(sample_name, monitorWS,
        StartWorkspaceIndex = str(MONITORSPECTRUM - 1), EndWorkspaceIndex = str(MONITORSPECTRUM - 1))
    if INSTR_NAME == 'LOQ':
        RemoveBins(monitorWS, monitorWS, '19900', '20500', Interpolation="Linear")
    
    # Remove flat background
    if BACKMON_START != None and BACKMON_END != None:
        FlatBackground(monitorWS, monitorWS, StartX = BACKMON_START, EndX = BACKMON_END, WorkspaceIndexList = '0')
    
    # Get the bank we are looking at
    final_result = run_setup.getReducedWorkspace()
    CropWorkspace(sample_name, final_result,
        StartWorkspaceIndex = (SPECMIN - 1), EndWorkspaceIndex = str(SPECMAX - 1))
    #####################################################################################
        
    ########################## Masking  ################################################
    # Mask the corners and beam stop if radius parameters are given
    maskpt_rmin = run_setup.getMaskPtMin()
    maskpt_rmax = run_setup.getMaskPtMax()
    if finding_centre == True:
        if RMIN > 0.0: 
            SANSUtility.MaskInsideCylinder(final_result, RMIN, maskpt_rmin[0], maskpt_rmin[1])
        if RMAX > 0.0:
            SANSUtility.MaskOutsideCylinder(final_result, RMAX, maskpt_rmin[0], maskpt_rmin[1])
    else:
        if RMIN > 0.0: 
            SANSUtility.MaskInsideCylinder(final_result, RMIN, maskpt_rmin[0], maskpt_rmin[1])
        if RMAX > 0.0:
            SANSUtility.MaskOutsideCylinder(final_result, RMAX, maskpt_rmax[0], maskpt_rmax[1])

    applyMasking(final_result, SPECMIN, DIMENSION, orientation,True)
    ####################################################################################

    ######################## Unit change and rebin #####################################
    # Convert all of the files to wavelength and rebin
    # ConvertUnits does have a rebin option, but it's crude. In particular it rebins on linear scale.
    ConvertUnits(monitorWS, monitorWS, "Wavelength")
    wavbin =  str(wav_start) + "," + str(DWAV) + "," + str(wav_end)
    if SAMP_INTERPOLATE :
        InterpolatingRebin(monitorWS, monitorWS,wavbin)
    else :
        Rebin(monitorWS, monitorWS,wavbin)
        
    ConvertUnits(final_result,final_result,"Wavelength")
    Rebin(final_result,final_result,wavbin)
    ####################################################################################

    ####################### Correct by incident beam monitor ###########################
    # At this point need to fork off workspace name to keep a workspace containing raw counts
    tmpWS = "reduce_temp_workspace"
    Divide(final_result, monitorWS, tmpWS)
    mantid.deleteWorkspace(monitorWS)
    ###################################################################################

    ############################ Transmission correction ##############################
    trans_ws = CalculateTransmissionCorrection(run_setup, wav_start, wav_end, use_def_trans)
    if trans_ws != None:
        Divide(tmpWS, trans_ws, tmpWS)
    ##################################################################################   
        
    ############################ Efficiency correction ################################
    if DETBANK == 'rear-detector' or 'main-detector-bank':
        CorrectToFile(tmpWS, DIRECT_BEAM_FILE_R, tmpWS, "Wavelength", "Divide")
    else:
        CorrectToFile(tmpWS, DIRECT_BEAM_FILE_F, tmpWS, "Wavelength", "Divide")
    ###################################################################################
        
    ############################# Scale by volume #####################################
    scalefactor = RESCALE
    # Data reduced with Mantid is a factor of ~pi higher than colette.
    # For LOQ only, divide by this until we understand why.
    if INSTR_NAME == 'LOQ':
        rescaleToColette = math.pi
        scalefactor /= rescaleToColette
    
    SANSUtility.ScaleByVolume(tmpWS, scalefactor, SAMPLE_GEOM, SAMPLE_WIDTH, SAMPLE_HEIGHT, SAMPLE_THICKNESS)
    ################################################## ################################
        
    ################################ Correction in Q space ############################
    # 1D
    if CORRECTION_TYPE == '1D':
        if finding_centre == True:
            GroupIntoQuadrants(tmpWS, final_result, maskpt_rmin[0], maskpt_rmin[1], Q_REBIN)
            return
        else:
            Q1D(tmpWS,final_result,final_result,Q_REBIN, AccountForGravity=GRAVITY)
    # 2D    
    else:
        # Run 2D algorithm
        Qxy(tmpWS, final_result, QXY2, DQXY)

    mantid.deleteWorkspace(tmpWS)
    return
############################# End of Correct function ###################################################

############################ Centre finding functions ###################################################

# These variables keep track of the centre coordinates that have been used so that we can calculate a relative shift of the
# detector
XVAR_PREV = 0.0
YVAR_PREV = 0.0
ITER_NUM = 0
RESIDUE_GRAPH = None
                
# Create a workspace with a quadrant value in it 
def CreateQuadrant(reduced_ws, rawcount_ws, quadrant, xcentre, ycentre, q_bins, output):
    # Need to create a copy because we're going to mask 3/4 out and that's a one-way trip
    CloneWorkspace(reduced_ws,output)
    objxml = SANSUtility.QuadrantXML([xcentre, ycentre, 0.0], RMIN, RMAX, quadrant)
    # Mask out everything outside the quadrant of interest
    MaskDetectorsInShape(output,objxml)
    # Q1D ignores masked spectra/detectors. This is on the InputWorkspace, so we don't need masking of the InputForErrors workspace
    Q1D(output,rawcount_ws,output,q_bins,AccountForGravity=GRAVITY)

    flag_value = -10.0
    ReplaceSpecialValues(InputWorkspace=output,OutputWorkspace=output,NaNValue=flag_value,InfinityValue=flag_value)
    if CORRECTION_TYPE == '1D':
        SANSUtility.StripEndZeroes(output, flag_value)

# Create 4 quadrants for the centre finding algorithm and return their names
def GroupIntoQuadrants(reduced_ws, final_result, xcentre, ycentre, q_bins):
    tmp = 'quad_temp_holder'
    pieces = ['Left', 'Right', 'Up', 'Down']
    to_group = ''
    counter = 0
    for q in pieces:
        counter += 1
        to_group += final_result + '_' + str(counter) + ','
        CreateQuadrant(reduced_ws, final_result, q, xcentre, ycentre, q_bins, final_result + '_' + str(counter))

    # We don't need these now
    mantid.deleteWorkspace(reduced_ws)

# Calcluate the sum squared difference of the given workspaces. This assumes that a workspace with
# one spectrum for each of the quadrants. The order should be L,R,U,D.
def CalculateResidue():
    global XVAR_PREV, YVAR_PREV, RESIDUE_GRAPH
    yvalsA = mtd.getMatrixWorkspace('Left').readY(0)
    yvalsB = mtd.getMatrixWorkspace('Right').readY(0)
    qvalsA = mtd.getMatrixWorkspace('Left').readX(0)
    qvalsB = mtd.getMatrixWorkspace('Right').readX(0)
    qrange = [len(yvalsA), len(yvalsB)]
    nvals = min(qrange)
    residueX = 0
    indexB = 0
    for indexA in range(0, nvals):
        if qvalsA[indexA] < qvalsB[indexB]:
            mantid.sendLogMessage("::SANS::LR1 "+str(indexA)+" "+str(indexB))
            continue
        elif qvalsA[indexA] > qvalsB[indexB]:
            while qvalsA[indexA] > qvalsB[indexB]:
                mantid.sendLogMessage("::SANS::LR2 "+str(indexA)+" "+str(indexB))
                indexB += 1
        if indexA > nvals - 1 or indexB > nvals - 1:
            break
        residueX += pow(yvalsA[indexA] - yvalsB[indexB], 2)
        indexB += 1

    yvalsA = mtd.getMatrixWorkspace('Up').readY(0)
    yvalsB = mtd.getMatrixWorkspace('Down').readY(0)
    qvalsA = mtd.getMatrixWorkspace('Up').readX(0)
    qvalsB = mtd.getMatrixWorkspace('Down').readX(0)
    qrange = [len(yvalsA), len(yvalsB)]
    nvals = min(qrange)
    residueY = 0
    indexB = 0
    for indexA in range(0, nvals):
        if qvalsA[indexA] < qvalsB[indexB]:
            mantid.sendLogMessage("::SANS::UD1 "+str(indexA)+" "+str(indexB))
            continue
        elif qvalsA[indexA] > qvalsB[indexB]:
            while qvalsA[indexA] > qvalsB[indexB]:
                mantid.sendLogMessage("::SANS::UD2 "+str(indexA)+" "+str(indexB))
                indexB += 1
        if indexA > nvals - 1 or indexB > nvals - 1:
            break
        residueY += pow(yvalsA[indexA] - yvalsB[indexB], 2)
        indexB += 1
                        
    if RESIDUE_GRAPH is None or (not RESIDUE_GRAPH in appwidgets()):
        RESIDUE_GRAPH = plotSpectrum('Left', 0)
        mergePlots(RESIDUE_GRAPH, plotSpectrum(['Right','Up'],0))
        mergePlots(RESIDUE_GRAPH, plotSpectrum(['Down'],0))
    RESIDUE_GRAPH.activeLayer().setTitle("Itr " + str(ITER_NUM)+" "+str(XVAR_PREV*1000.)+","+str(YVAR_PREV*1000.)+" SX "+str(residueX)+" SY "+str(residueY))

    mantid.sendLogMessage("::SANS::Itr: "+str(ITER_NUM)+" "+str(XVAR_PREV*1000.)+","+str(YVAR_PREV*1000.)+" SX "+str(residueX)+" SY "+str(residueY))              
    return residueX, residueY
	
def RunReduction(coords):
    '''Compute the value of (L-R)^2+(U-D)^2 a circle split into four quadrants'''
    global XVAR_PREV, YVAR_PREV
    xcentre = coords[0]
    ycentre= coords[1]
    
    xshift = -xcentre + XVAR_PREV
    yshift = -ycentre + YVAR_PREV
    XVAR_PREV = xcentre
    YVAR_PREV = ycentre

    # Do the correction
    if xshift != 0.0 or yshift != 0.0:
        MoveInstrumentComponent(SCATTER_SAMPLE.getName(), ComponentName = DETBANK, X = str(xshift), Y = str(yshift), RelativePosition="1")
        if SCATTER_CAN.getName() != '':
            MoveInstrumentComponent(SCATTER_CAN.getName(), ComponentName = DETBANK, X = str(xshift), Y = str(yshift), RelativePosition="1")
			
    _SAMPLE_SETUP.setMaskPtMin([0.0,0.0])
    _SAMPLE_SETUP.setMaskPtMax([xcentre, ycentre])
    if _CAN_SETUP != None:
        _CAN_SETUP.setMaskPtMin([0.0, 0.0])
        _CAN_SETUP.setMaskPtMax([xcentre, ycentre])

    WavRangeReduction(WAV1, WAV2, DefaultTrans, finding_centre = True)
    return CalculateResidue()

def FindBeamCentre(rlow, rupp, MaxIter = 10, xstart = None, ystart = None):
    global XVAR_PREV, YVAR_PREV, ITER_NUM, RMIN, RMAX, XBEAM_CENTRE, YBEAM_CENTRE
    RMIN = float(rlow)/1000.
    RMAX = float(rupp)/1000.

    if xstart == None or ystart == None:
        XVAR_PREV = XBEAM_CENTRE
        YVAR_PREV = YBEAM_CENTRE
    else:
        XVAR_PREV = xstart
        YVAR_PREV = ystart

    mantid.sendLogMessage("::SANS:: xstart,ystart="+str(XVAR_PREV*1000.)+" "+str(YVAR_PREV*1000.)) 
    _printMessage("Starting centre finding routine ...")
    # Initialize the workspace with the starting coordinates. (Note that this moves the detector to -x,-y)
    _initReduction(XVAR_PREV, YVAR_PREV)

    ITER_NUM = 0
    # Run reduction, returning the X and Y sum-squared difference values 
    _printMessage("Running initial reduction: " + str(XVAR_PREV*1000.)+ "  "+ str(YVAR_PREV*1000.))
    oldX2,oldY2 = RunReduction([XVAR_PREV, YVAR_PREV])
    XSTEP = 5.0/1000.
    YSTEP = 5.0/1000.
    # take first trial step
    XNEW = XVAR_PREV + XSTEP
    YNEW = YVAR_PREV + YSTEP
    for ITER_NUM in range(1, MaxIter+1):
        _printMessage("Iteration " + str(ITER_NUM) + ": " + str(XNEW*1000.)+ "  "+ str(YNEW*1000.))
        newX2,newY2 = RunReduction([XNEW, YNEW])
        if newX2 > oldX2:
            XSTEP = -XSTEP/2.
        if newY2 > oldY2:
            YSTEP = -YSTEP/2.
        if abs(XSTEP) < 0.1251/1000. and abs(YSTEP) < 0.1251/1000. :
            _printMessage("::SANS:: Converged - check if stuck in local minimum!")
            break
        oldX2 = newX2
        oldY2 = newY2
        XNEW += XSTEP
        YNEW += YSTEP
	
    if ITER_NUM == MaxIter:
        _printMessage("::SANS:: Out of iterations, new coordinates may not be the best!")
        XNEW -= XSTEP
        YNEW -= YSTEP

    
    XBEAM_CENTRE = XNEW
    YBEAM_CENTRE = YNEW
    _printMessage("Centre coordinates updated: [" + str(XBEAM_CENTRE*1000.)+ ","+ str(YBEAM_CENTRE*1000.) + ']')
    
    # Reload the sample and can and reset the radius range
    global _SAMPLE_SETUP
    _assignHelper(_SAMPLE_RUN, False, PERIOD_NOS["SCATTER_SAMPLE"])
    _SAMPLE_SETUP = None
    if _CAN_RUN != '':
        _assignHelper(_CAN_RUN, False, PERIOD_NOS["SCATTER_CAN"])
        global _CAN_SETUP
        _CAN_SETUP = None
    
    RMIN = DEF_RMIN
    RMAX = DEF_RMAX

##
# Plot the results on the correct type of plot
##
def PlotResult(workspace):
    if CORRECTION_TYPE == '1D':
        plotSpectrum(workspace,0)
    else:
        qti.app.mantidUI.importMatrixWorkspace(workspace).plotGraph2D()

##################### View mask details #####################################################

def ViewCurrentMask():
    top_layer = 'CurrentMask'
    LoadEmptyInstrument(INSTR_DIR + '/' + INSTR_NAME + "_Definition.xml",top_layer)
    if RMIN > 0.0: 
        SANSUtility.MaskInsideCylinder(top_layer, RMIN, XBEAM_CENTRE, YBEAM_CENTRE)
    if RMAX > 0.0:
        SANSUtility.MaskOutsideCylinder(top_layer, RMAX, 0.0, 0.0)
    
    if INSTR_NAME == "SANS2D":
        firstspec = 5
    else:
        firstspec = 3

    dimension = SANSUtility.GetInstrumentDetails(INSTR_NAME, DETBANK)[0]
    applyMasking(top_layer, firstspec, dimension, SANSUtility.Orientation.HorizontalFlipped, False)
    
    # Mark up "dead" detectors with error value 
    FindDeadDetectors(top_layer, top_layer, DeadValue=500)

    # Visualise the result
    instrument_win = qti.app.mantidUI.getInstrumentView(top_layer)
    instrument_win.showWindow()

############################################################################################################################

############################################################################################
# Print a test script for Colette if asked
def createColetteScript(inputdata, format, reduced, centreit , plotresults, csvfile = '', savepath = ''):
    script = ''
    if csvfile != '':
        script += '[COLETTE]  @ ' + csvfile + '\n'
    file_1 = inputdata['sample_sans'] + format
    script += '[COLETTE]  ASSIGN/SAMPLE ' + file_1 + '\n'
    file_1 = inputdata['sample_trans'] + format
    file_2 = inputdata['sample_direct_beam'] + format
    if file_1 != format and file_2 != format:
        script += '[COLETTE]  TRANSMISSION/SAMPLE/MEASURED ' + file_1 + ' ' + file_2 + '\n'
    file_1 = inputdata['can_sans'] + format
    if file_1 != format:
        script +='[COLETTE]  ASSIGN/CAN ' + file_1 + '\n'
    file_1 = inputdata['can_trans'] + format
    file_2 = inputdata['can_direct_beam'] + format
    if file_1 != format and file_2 != format:
        script += '[COLETTE]  TRANSMISSION/CAN/MEASURED ' + file_1 + ' ' + file_2 + '\n'
    if centreit:
        script += '[COLETTE]  FIT/MIDDLE'
    # Parameters
    script += '[COLETTE]  LIMIT/RADIUS ' + str(RMIN) + ' ' + str(RMAX) + '\n'
    script += '[COLETTE]  LIMIT/WAVELENGTH ' + str(WAV1) + ' ' + str(WAV2) + '\n'
    if DWAV <  0:
        script += '[COLETTE]  STEP/WAVELENGTH/LOGARITHMIC ' + str(DWAV)[1:] + '\n'
    else:
        script += '[COLETTE]  STEP/WAVELENGTH/LINEAR ' + str(DWAV) + '\n'
    # For the moment treat the rebin string as min/max/step
    qbins = q_REBEIN.split(",")
    nbins = len(qbins)
    if CORRECTION_TYPE == '1D':
        script += '[COLETTE]  LIMIT/Q ' + str(qbins[0]) + ' ' + str(qbins[nbins-1]) + '\n'
        dq = float(qbins[1])
        if dq <  0:
            script += '[COLETTE]  STEP/Q/LOGARITHMIC ' + str(dq)[1:] + '\n'
        else:
            script += '[COLETTE]  STEP/Q/LINEAR ' + str(dq) + '\n'
    else:
        script += '[COLETTE]  LIMIT/QXY ' + str(0.0) + ' ' + str(QXY2) + '\n'
        if DQXY <  0:
            script += '[COLETTE]  STEP/QXY/LOGARITHMIC ' + str(DQXY)[1:] + '\n'
        else:
            script += '[COLETTE]  STEP/QXY/LINEAR ' + str(DQXY) + '\n'
    
    # Correct
    script += '[COLETTE] CORRECT\n'
    if plotresults:
        script += '[COLETTE]  DISPLAY/HISTOGRAM ' + reduced + '\n'
    if savepath != '':
        script += '[COLETTE]  WRITE/LOQ ' + reduced + ' ' + savepath + '\n'
        
    return script

############################################################################################
