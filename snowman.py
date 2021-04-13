#!/usr/bin/env python
#
# This example creates a polygonal model of a cone, and then renders it to
# the screen. It will rotate the cone 360 degrees and then exit. The basic
# setup of source -> mapper -> actor -> renderer -> renderwindow is
# typical of most VTK programs.
#

#
# First we include the VTK Python packages that will make available
# all of the VTK commands to Python.
#
import vtk as vtk
import time

#
# Next we create an instance of vtkConeSource and set some of its
# properties. The instance of vtkConeSource "cone" is part of a visualization
# pipeline (it is a source process object); it produces data (output type is
# vtkPolyData) which other filters may process.
#
body = vtk.vtkSphereSource()
body.SetCenter(0, 0, 0)
body.SetRadius( 2.0 )
body.SetThetaResolution(15)
body.SetPhiResolution(15)

head = vtk.vtkSphereSource()
head.SetCenter(-4, 0, 0)
head.SetRadius( 1.5 )
head.SetThetaResolution(15)
head.SetPhiResolution(15)

leftEye = vtk.vtkSphereSource()
leftEye.SetCenter(0.5, 3.5, 1.3)
leftEye.SetRadius( 0.2 )
leftEye.SetThetaResolution(15)
leftEye.SetPhiResolution(15)

rightEye = vtk.vtkSphereSource()
rightEye.SetCenter(-0.5, 3.5, 1.3)
rightEye.SetRadius( 0.2 )
rightEye.SetThetaResolution(15)
rightEye.SetPhiResolution(15)

nose = vtk.vtkConeSource()
nose.SetCenter(4, 0, 0)
nose.SetDirection(0, -1, 0)
nose.SetHeight( 0.5 )
nose.SetRadius( 0.1 )
nose.SetResolution(20)


#
# In this example we terminate the pipeline with a mapper process object.
# (Intermediate filters such as vtkShrinkPolyData could be inserted in
# between the source and the mapper.)  We create an instance of
# vtkPolyDataMapper to map the polygonal data into graphics primitives. We
# connect the output of the cone souece to the input of this mapper.
#
headMapper = vtk.vtkPolyDataMapper()
headMapper.SetInputConnection( head.GetOutputPort() )

bodyMapper = vtk.vtkPolyDataMapper()
bodyMapper.SetInputConnection( body.GetOutputPort() )

noseMapper = vtk.vtkPolyDataMapper()
noseMapper.SetInputConnection( nose.GetOutputPort() )

leftEyeMapper = vtk.vtkPolyDataMapper()
leftEyeMapper.SetInputConnection( leftEye.GetOutputPort() )

rightEyeMapper = vtk.vtkPolyDataMapper()
rightEyeMapper.SetInputConnection( rightEye.GetOutputPort() )

#
# Create an actor to represent the cone. The actor orchestrates rendering of
# the mapper's graphics primitives. An actor also refers to properties via a
# vtkProperty instance, and includes an internal transformation matrix. We
# set this actor's mapper to be coneMapper which we created above.
#
headActor = vtk.vtkActor()
headActor.SetMapper( headMapper )

bodyActor = vtk.vtkActor()
bodyActor.SetMapper( bodyMapper )

noseActor = vtk.vtkActor()
noseActor.SetMapper( noseMapper )
noseActor.GetProperty().SetColor(255, 165, 0)

leftEyeActor = vtk.vtkActor()
leftEyeActor.SetMapper( leftEyeMapper )
leftEyeActor.GetProperty().SetColor(0, 0, 0)
leftEyeActor.SetVisibility(False)

rightEyeActor = vtk.vtkActor()
rightEyeActor.SetMapper( rightEyeMapper )
rightEyeActor.GetProperty().SetColor(0, 0, 0)
rightEyeActor.SetVisibility(False)

#
# Create the Renderer and assign actors to it. A renderer is like a
# viewport. It is part or all of a window on the screen and it is
# responsible for drawing the actors it has.  We also set the background
# color here
#
ren1= vtk.vtkRenderer()
ren1.AddActor( headActor )
ren1.AddActor( bodyActor )
ren1.AddActor(noseActor)
ren1.AddActor(leftEyeActor)
ren1.AddActor(rightEyeActor)
ren1.SetBackground( 0.1, 0.2, 0.4 )
ren1.GetActiveCamera().SetFocalPoint(0,0,0)
ren1.GetActiveCamera().SetPosition(0,0,22)

#
# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We also
# set the size to be 300 pixels by 300
#
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer( ren1 )
renWin.SetSize( 500, 500 )


for i in range(0,90):
    time.sleep(0.01)
    renWin.Render()
    ren1.GetActiveCamera().Azimuth(1)

#
# rotate head to over the body
# 0:00 - 0:03
#
for i in range (0, 90):
    time.sleep(0.03)
    headActor.RotateZ(-1)
    renWin.Render()

#
# lower the head into the body
# 0:03 - 0:06
#
lower = vtk.vtkTransform()
headActor.SetUserTransform(lower)
for i in range (0, 80):
    time.sleep(0.01)
    lower.Translate(0, -0.01, 0)
    renWin.Render()


#
# rotate the nose in front of the body
# 0:06 - 0:09
#
for i in range (0, 90):
    time.sleep(0.03)
    noseActor.RotateY(-1)
    renWin.Render()


headActor.SetVisibility(False)

#
# bring the nose closer to the body
# 0:09 - 0:11
#
noseTranslate = vtk.vtkTransform()
noseActor.SetUserTransform(noseTranslate)
for i in range (0, 80):
    time.sleep(0.01)
    noseTranslate.Translate(0, 0, -0.01)
    renWin.Render()

# neutral = vtk.vtkTransform()
# noseActor.SetUserTransform(neutral)

#
# rotate the nose into the head
# 0:11 - 0:14
#
noseActor.SetOrigin(0, 0, 0)

for i in range (0, 90):
    time.sleep(0.03)
    #noseActor.RotateWXYZ(1, 0, 0, 1)
    noseActor.RotateZ(1)
    renWin.Render()

#
# bring the nose at the surface of the face
# 0:14 - 0:16
#
noseActor.SetUserTransform(noseTranslate)
for i in range (0, 175):
    time.sleep(0.01)
    noseTranslate.Translate(0, 0, 0.01)
    renWin.Render()


# 
# Adding eyes - 0:16
#
leftEyeActor.SetVisibility(True)
rightEyeActor.SetVisibility(True)

#
# 0:16 - 0:22
#
for i in range(0,360):
    time.sleep(0.01)

    renWin.Render()
    ren1.GetActiveCamera().Roll(1)

#
# 0:22 - 0:28
#
for i in range(0,360):
    time.sleep(0.01)

    renWin.Render()
    ren1.GetActiveCamera().Azimuth(1)


#
# 0:28 - 0:31
#
for i in range(0,80):
    time.sleep(0.03)

    renWin.Render()
    ren1.GetActiveCamera().Elevation(1)

#
# 0:31 - 0:34
#
for i in range(0,80):
    time.sleep(0.03)

    renWin.Render()
    ren1.GetActiveCamera().Elevation(-1)
