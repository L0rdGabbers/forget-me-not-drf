
# Forget Me Not - DRF API
## Site Overview

# Table of Contents
* [Forget Me Not - DRF API](#forget-me-not---drf-api)
  * [Site Overview](#site-overview)
* [Table of Contents](#table-of-contents)
* [Design](#design)
* [Agile Methodology](#agile-methodology)
  * [Overview](#overview)
    * [Sprint 1 notes](#sprint-1-notes)
    * [Sprint 2 notes](#sprint-2-notes)
    * [Major Remaining Changes](#major-remaining-changes)
* [Planning](#planning)
  * [Site Aims](#site-aims)
  * [User Stories](#user-stories)
    * [Unsuccessful User Stories](#unsuccessful-user-stories)
  * [Data Model](#data-model)
* [Agile Methodology](#agile-methodology-1)
  * [Overview](#overview-1)
    * [Sprint 1 notes](#sprint-1-notes-1)
    * [Sprint 2 notes](#sprint-2-notes-1)
    * [Sprint 3 notes](#sprint-3-notes)
    * [Major remaining changes](#major-remaining-changes-1)
* [Serialized Data](#serialized-data)
  * [Note](#note)
  * [Profiles](#profiles)
    * [List](#list)
    * [Details](#details)
  * [Friends](#friends)
    * [List](#list-1)
    * [Detail](#detail)
    * [Send Friend Request](#send-friend-request)
    * [Friend Requests List](#friend-requests-list)
    * [Friend Request Detail](#friend-request-detail)
  * [Projects](#projects)
    * [List](#list-2)
    * [Detail](#detail-1)
  * [Tasks](#tasks)
    * [List](#list-3)
    * [Detail](#detail-2)
* [Verification](#verification)


# **Planning**

## **Site Aims**

The Forget Me Not site had two main goals:

1. To allow people to organise their big life or work projects into a clear and categorised space.
2. To provide a place for people to work together by providing the opportunity to allocate project tasks to specific collaborators.

## **User Stories**
The following user stories are sourced from the front end repository; these ones are backend specific, since they involve interfacing between the front end and the back end to handle data.

- As a User, I can sign into my profile so that I can access my projects, tasks, and friends list.
- As a logged in user, I can create projects so that I can organise myself and set clear deadlines.
- As a user, I can view the details of my projects or projects that I'm a colaborator of so that I can see the tasks and deadlines of the project.
- As a logged in user, I can create tasks associated to my projects so that I can break up my projects into bite-sized chunks.
- As a logged in user, I can view my projects' tasks or tasks that I'm associated with so that I can the tasks details.
- As an owner of a project, I can edit or delete my projects or their assoicated tasks so that I can edit or remove any mistakes in any of my projects.
- As a logged in user, I can send a friend request to another user so that I can make them collaborators on my future projects.
- As a user, I can accept or decline any friend requests that were sent to me so that I can confirm whether I want a particular user to work on my projects.
- As a user, I can cancel any friend requests that I sent before they are accepted by the recipient so that I can prevent people that I didn't mean to send requests from seeing my request in the first place.
- As a logged in user, I can see a list of my friends so that I can decide who should be collaborators on my projects and tasks.
- As a project owner, I can edit my projects and tasks so that I can change my projects' collaborators or change any neccessary details regarding the project.
- As a project owner, I can confirm that a project is complete so that I can remove it from my todo projects.
- As a project owner or task collaborator, I can confirm that a task is complete so that I can mark a project's task's completion status is positive.
- As a user, I can view other users' profile pages so that I can see if I want to send them a friend request, or view our friendship status.
- As a user, I can edit my profile page so that I can add my own bio and profile image.

### **Unsuccessful User Stories**

- As a user, I can message my friends or fellow collaborators so that I can keep work related discussions in one location.
  - A message model could have been created, but when I had thought of a way to code this user story, the project was already too far in development to incorporate it.

- As a user, I can attatch a file, such as a word document or a powerpoint file so that I can allow other collaborators to view the work I have done.
  - As discussed in the agile sprint section, I had decided to remove file sharing as a feature do to the frustrating nature of the file field.

## **Data Model**

To challenge myself, instead of making two only models (project and task), I decided to also add a friend model, since many websites have a friend system and I thought it would be a good challenge to incorporate one into this site. Furthermore, it seems like a crucial feature, that way tasks can be shared and workloads lightened.

The following image shows the original entity relationship diagram that I had come up with when envisioning the site.

![Original model](/assets/original-database.jpg)

However, further into development, I had learnt that making two friend models, Friend List and Friend Request, would be a much more approachable. I also included a new field, Bio to the profile model.

![Updated model](/assets/final-database-model.jpg)

Both of these models were created using https://www.drawio.com/

# **Agile Methodology**
## **Overview**

This section will specifically discuss the back end for this project.
For the frontend, please visit the [Forget Me Not React Repository](https://github.com/L0rdGabbers/forget-me-not-react).

### Sprint 1 notes
For my first sprint of 3 days, I had decided on designing the wireframes for the frontend and model framework for the backend, since I also had a commitment to rehearsing a play.
#### 24/11/23 - 26/11/23
* During this process I had decided to include a friend model, so that only friends would be able to colaborate with each other and so as to not be spammed by unknown users. I also included the Project and Task model so that bigger pieces of work could be made into smaller bite sizes. This made the app more of a team building web application rather than a reminding app, which felt much more applicable.

### Sprint 2 notes
This sprint mainly focused on creating the required apps.
#### 28/11/23 
* Create the Profiles app.
* Successfully implement logging in and logging out functionality. 
* Creates Profiles List and Detail views.
#### 30/11/23
* Create the Friends app. Instead of a single model, however, the friends/models.py contains two models, one is a user's personal and unique friend list and the other is a friend request model.
#### 1/12/23
* Creates the Projects app.
#### 2/12/23
* Creates the Tasks app.

### Sprint 3 notes
Once the apps were all created, all that remained was to tidy up the functions so that there weren't any hidden issues and prepared the app for deployment.
#### 5/12/23
* Adds unfriend functionality to the friends views.
#### 7/12/23
* Adds JSON web token functionality, to ensure that the user isn't logged out every five minutes.
* Adds code to ensure that unsafe methods (PUT, DELETE) are can only be performed by an object's owner (or in some situations, a collaborator).
* The file field was removed from the tasks model. Since it was listed as a Could Have feature, and it was taking up to much time to implement, I had decided to leave it alone until I was in a more secure place.
#### 9/12/23
* Deploys API to Heroku for the first time.
* Sets up the deployed Front End site, and development front end site as the Client Origin and Client Origin Dev sites, respectively.

### Major remaining changes
At this point, my main focus was on the front end of the site, however there are some important changes I made along the way in order to reorganise the way the data was serialised to the front end.

#### Debug Mode - 12/12/23
In order to see how the backend data might not have been properly configured, I imported heroku debug mode so that I could see what was causing the error in the backend through the frontend.

#### Current User Serialzer - 13/12/23
Updates the current user serializer to return the user's whole profile model instead of a variant with slightly different working (id instead of pk, etc. etc.)

#### Data Pagination Bug - 15/12/23
Removes the rest framework pagination, since it was preventing complete lists of data from being rendered to the front end.

#### Bio Field - 21/12/23
Added a new field, Bio, to the Profile model, to allow a user to write something about themselves that will appear on their profile page.

# Serialized Data 

## Note
In order to make the serialized views a bit more visually appealing, I have opted to use the Debug mode = True to display the data in a bit more clear fashion.

## Profiles

### List

This List returns all of the created user profiles.

![Profile List](/assets/profile-list.png)

### Details

This will return a specified user's profile data.

![Profile Data](/assets/profile-data.png)

If the user is a profile's owner, they will be able to edit their profile data. The delete method is not an option for this model.

![Profile Data - Owner](/assets/profile-data-owner.png)

## Friends

### List

This list returns a user's friends.

![Friend List](/assets/friend-list-drf.png)

### Detail

This page shows the friend details, which can only be viewed by the friend object's owner. This view is mainly for accessing the unfriend function.

![Friend Detail](/assets/friend-detail-drf.png)

If a user who is not the friend object's sender or receiver selects this view, it will return as 404 not found.

![Not your friend](/assets/not-user-friend.png)

### Send Friend Request

This is a POST request only page, and is used to send a friend request to a specified user profile

![Send Friend Request](/assets/send-friend-request.png)

If successful, it will return a 201 created response.

![Friend Request Send](/assets/201.png)

However, if the receiver has already received an active friend request from the user, sent the user an active friend request, or is in the user's friend list, it will return an error.

![Friend Request Not Allowed](/assets/already-sent-friend-request.png)

### Friend Requests List

This list view allows for the user to see any friend requests they have seen or received.

![Friend Requests List](/assets/friend-requests-drf.png)

### Friend Request Detail

This page allows for the user to accept or delete any request they have received, or cancel any request they have sent.

![Friend Request Sender](/assets/sender-drf.png)

![Friend Request Receiver](/assets/receiver-drf.png)

If the user is neither the request receiver or sender, then it returns error 404.

![Friend Request Not Found](/assets/request-not-found.png)

## Projects

### List

This list allows for the user to view projects that they own, or projects that they are collaborators of.

![Projects List Page](/assets/project-list-drf.png)

### Detail

This page allows for the user to view their project details as well as to edit their project.

![Projects Detail Page](/assets/project-detail-drf.png)

Collaborators are able to view the project they are associated with, but not to make PUT or DELETE requests.

![Projects Detail Page - Collaborator](/assets/project-detail-drf-collaborator.png)

## Tasks

### List

This list allows for the user to view tasks that they own, or that they are collaborators of.

![Tasks List Page](/assets/task-list-drf.png)

### Detail

This page allows for the user to view their task details as well as to edit their task.

![Tasks Detail Page](/assets/task-detail-drf.png)

Unlike the projects page, collaborators are permitted to make PUT requests to an object that they do not own. This is so that they are able to submit a project as complete. (In the front end, this is the only permission they are granted.)

![Tasks Detail Page](/assets/task-detail-drf-collaborator.png)

# Verification
