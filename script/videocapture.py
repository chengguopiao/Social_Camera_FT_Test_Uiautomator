#!/usr/bin/python
# coding:utf-8

from uiautomatorplug.android import device as d
import unittest
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import string

AD = util.Adb()
TB = util.TouchButton()
SM = util.SetMode() 

#Written by XuGuanjun

PACKAGE_NAME  = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

#All setting info of camera could be cat in the folder
PATH_PREF_XML  = '/data/data/com.intel.camera22/shared_prefs/'

#FDFR / GEO / BACK&FROUNT xml file in com.intelcamera22_preferences_0.xml
PATH_0XML      = PATH_PREF_XML + 'com.intel.camera22_preferences_0.xml'

#PICSIZE / EXPROSURE / TIMER / WHITEBALANCE / ISO / HITS / VIDEOSIZE in com.intel.camera22_preferences_0_0.xml
PATH_0_0XML    = PATH_PREF_XML + 'com.intel.camera22_preferences_0_0.xml'

#####                                    #####
#### Below is the specific settings' info ####
###                                        ###
##                                          ##
#                                            #

#FD/FR states check point
FDFR_STATE      = PATH_0XML   + ' | grep pref_fdfr_key'

#Geo state check point
GEO_STATE       = PATH_0XML   + ' | grep pref_camera_geo_location_key'

#Pic size state check point
PICSIZE_STATE   = PATH_0_0XML + ' | grep pref_camera_picture_size_key'

#Exposure state check point 
EXPOSURE_STATE  = PATH_0_0XML + ' | grep pref_camera_exposure_key'

#Timer state check point
TIMER_STATE     = PATH_0_0XML + ' | grep pref_camera_delay_shooting_key'

#Video Size state check point
VIDEOSIZE_STATE = PATH_0_0XML + ' | grep pref_video_quality_key'

#White balance state check point
WBALANCE_STATE  = PATH_0_0XML + ' | grep pref_camera_whitebalance_key'

#Flash state check point
FLASH_STATE     = PATH_0_0XML + ' | grep pref_camera_video_flashmode_key'

#SCENE state check point
SCENE_STATE     = PATH_0_0XML + ' | grep pref_camera_scenemode_key'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        AD.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        AD.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()
        SM.switchcamera('video')
        time.sleep(1)


    def tearDown(self):
    	AD.cmd('pm','com.intel.camera22') #Force reset the camera settings to default
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testRecordVideoWithFlashOn(self):
        '''
            Summary: Record a video in flash on mode
            Steps  : 
                1.Launch video activity
                2.Check flash state, set to ON
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video','flash','on')
        assert bool(AD.cmd('cat',FLASH_STATE).find('on')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithFlashOff(self):
        '''
            Summary: Record a video in flash off mode
            Steps  : 
                1.Launch video activity
                2.Check flash state, set to Off
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video','flash','off')
        assert bool(AD.cmd('cat',FLASH_STATE).find('off')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithBalanceAuto(self):
        '''
            Summary: Capture video with White Balance Auto
            Steps  :  
                1.Launch video activity
                2.Set White Balance Auto
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,5)
        assert bool(AD.cmd('cat',WBALANCE_STATE).find('auto')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithBalanceIncandescent(self):
        '''
            Summary: Capture video with White Balance Incandescent
            Steps  :  
                1.Launch video activity
                2.Set White Balance Incandescent
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,4)
        assert bool(AD.cmd('cat',WBALANCE_STATE).find('incandescent')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithBalanceDaylight(self):
        '''
            Summary: Capture video with White Balance Daylight
            Steps  :  
                1.Launch video activity
                2.Set White Balance Daylight
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''

        SM.setCameraSetting('video',5,3)
        assert bool(AD.cmd('cat',WBALANCE_STATE).find('incandescent')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithBalanceFluorescent(self):
        '''
            Summary: Capture video with White Balance Fluorescent
            Steps  :  
                1.Launch video activity
                2.Set White Balance Fluorescent
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''

        SM.setCameraSetting('video',5,2)
        assert bool(AD.cmd('cat',WBALANCE_STATE).find('fluorescent')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithBalanceCloudy(self):
        '''
            Summary: Capture video with White Balance Cloudy
            Steps  :  
                1.Launch video activity
                2.Set White Balance Cloudy
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,1)
        assert bool(AD.cmd('cat',WBALANCE_STATE).find('cloudy')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithExposureAuto(self):
        '''
            Summary: Capture video with Exposure auto
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure auto
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,3)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('0')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithExposure1(self):
        '''
            Summary: Capture video with Exposure 1
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure 1
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,4)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('3')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithExposure2(self):
        '''
            Summary: Capture video with Exposure 2
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure 2
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,5)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('6')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithExposureRed1(self):
        '''
            Summary: Capture video with Exposure -1
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure -1
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,2)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('-3')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithExposureRed2(self):
        '''
            Summary: Capture video with Exposure -2
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure -2
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,1)
        assert bool(AD.cmd('cat',EXPOSURE_STATE).find('-6')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithHSSize(self):
        '''
            Summary: Capture video with HS size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to HS
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''

        SM.setCameraSetting('video',3,3)
        # Need two check point due to the same value for video size when set HS/HD
        assert bool(AD.cmd('cat',VIDEOSIZE_STATE).find('5')+1)
        assert bool(AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('true')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithHDSize(self):
        '''
            Summary: Capture video with HD size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to HD
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''

        SM.setCameraSetting('video',3,2)
        # Need two check point due to the same value for video size when set HS/HD
        assert bool(AD.cmd('cat',VIDEOSIZE_STATE).find('5')+1)
        assert bool(AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('false')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithSDSize(self):
        '''
            Summary: Capture video with SD size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to SD
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,1)
        assert bool(AD.cmd('cat',VIDEOSIZE_STATE).find('4')+1)
        #assert bool(AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('false')
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithFHDSize(self):
        '''
            Summary: Capture video with FHD size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to FHD
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,4)
        # Need two check point due to the same value for video size when set FHD/FHS
        assert bool(AD.cmd('cat',VIDEOSIZE_STATE).find('6')+1)
        assert bool(AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('false')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoCaptureVideoWithFHSSize(self):
        '''
            Summary: Capture video with FHS size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to FHS
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,5)
        # Need two check point due to the same value for video size when set FHD/FHS
        assert bool(AD.cmd('cat',VIDEOSIZE_STATE).find('6')+1)
        assert bool(AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('true')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithGeoLocationOn(self):
        '''
            Summary: Record an video in GeoLocation On
            Steps  :  
                1.Launch video activity
                2.Check geo-tag ,set to ON
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',2,2)
        assert bool(AD.cmd('cat',GEO_STATE).find('on')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithGeoLocationOff(self):
        '''
            Summary: Record an video in GeoLocation Off
            Steps  :  
                1.Launch video activity
                2.Check geo-tag ,set to Off
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',2,1)
        assert bool(AD.cmd('cat',GEO_STATE).find('off')+1)
        self._takeVideoAndCheckCount()

    def testRearFaceRecordVideoWithGeoLocationOn(self):
        '''
            Summary: Record an video with rear face camera and set GeoLocation On
            Steps  :  
                1.Launch video activity
                2.Set to front face camera
                3.Check geo-tag,set to ON
                4.Touch shutter button to capture 30s video
                5.Exit  activity
        '''
        TB.switchBackOrFrontCamera('front')
        SM.setCameraSetting('fvideo',1,2)
        assert bool(AD.cmd('cat',GEO_STATE).find('on')+1)
        self._takeVideoAndCheckCount()

    def testRearFaceRecordVideoWithGeoLocationOff(self):
        '''
            Summary: Record an video with rear face camera and set GeoLocation Off
            Steps  :  
                1.Launch video activity
                2.Set to front face camera
                3.Check geo-tag,set to Off
                4.Touch shutter button to capture 30s video
                5.Exit  activity
        '''
        TB.switchBackOrFrontCamera('front')
        SM.setCameraSetting('fvideo',1,1)
        time.sleep(1)
        assert bool(AD.cmd('cat',GEO_STATE).find('off')+1)
        self._takeVideoAndCheckCount()

    def testRecordVideoWithCaptureImage(self):
        '''
            Summary: Capture image when record video
            Steps  :  
                1.Launch video activity
                2.Touch shutter button to capture 30s video
                3.Touch screen to capture a picture during recording video
                4.Exit  activity 
        '''
        #No setting to be changed
        self._takeVideoAndCheckCount(capturetimes=5)

    def _takeVideoAndCheckCount(self,recordtime=30,delaytime=2,capturetimes=0):
        beforeNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takeVideo(recordtime,capturetimes)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - capturetimes - 1: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        #When it is the first time to launch camera there will be a dialog to ask user 'remember location', so need to check
        try:
            assert d(text = 'OK').wait.exists(timeout = 2000)
            d(text = 'OK').click.wait()
        except:
            pass
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(0,touchtimes):
            d.press('back')