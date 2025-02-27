"""Entity.py: contains the Entity class"""

from direct.showbase.DirectObject import DirectObject
from otp.otpbase.PythonUtil import lineInfo
import string
from direct.directnotify import DirectNotifyGlobal

class Entity(DirectObject):
    """
    Entity is the base class for all objects that exist in a Level
    and can be edited with the LevelEditor.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('Entity')

    def __init__(self, level=None, entId=None):
        self.initializeEntity(level, entId)

    def initializeEntity(self, level, entId):
        ###
        ### THIS IS WHERE ENTITIES GET THEIR ATTRIBUTES SET
        ###
        """
        Distributed entities on the client don't know their level or
        entId values until they've been generated, so they call this
        after they've been generated. At that point, the entity is good
        to go.
        """
        self.level = level
        self.entId = entId
        if (self.level is not None) and (self.entId is not None):
            self.level.initializeEntity(self)

    def __str__(self):
        if hasattr(self, 'level') and self.level:
            return 'ent%s(%s)' % (self.entId, self.level.getEntityType(self.entId))
        elif hasattr(self, 'name'):
            return self.name
        elif hasattr(self, 'entId'):
            return '%s-%s' % (self.__class__.__name__, self.entId)
        else:
            return self.__class__.__name__
            
    def destroy(self):
        """
        This is called when the level wants this entity to go away.
        Once this is called, the Entity should be considered defunct.
        NOTE: distributed entities are still valid distributed objects
        after this is called, but they are no longer valid entities.
        Distributed entities ought to be disabled and/or deleted shortly
        after this is called.
        """
        Entity.notify.debug('Entity.destroy() %s' % self.entId)
        # client-side distributed entities might be doing this after
        # the level has been been destroyed...?
        if self.level:
            if self.level.isInitialized():
                self.level.onEntityDestroy(self.entId)
            else:
                Entity.notify.warning('Entity %s destroyed after level??' %
                                      self.entId)
        self.ignoreAll()
        del self.level
        del self.entId
        
    def getUniqueName(self, name, entId=None):
        """returns a name that is unique for a particular entity;
        defaults to this entity"""
        if entId is None:
            entId = self.entId
        return '%s-%s-%s' % (name, self.level.levelId, entId)

    def getParentToken(self):
        """returns a value that uniquely identifies this entity for purposes
        of distributed parenting"""
        # give the level the option of modifying our entId, to handle instances
        # where there are multiple levels present on the client simultaneously
        return self.level.getParentTokenForEntity(self.entId)

    def getOutputEventName(self, entId=None):
        """returns the event generated by an entity; defaults to this entity"""
        if entId is None:
            entId = self.entId
        return self.getUniqueName('entityOutput', entId)

    def getZoneEntId(self):
        """returns entId of zone that contains this entity"""
        return self.level.getEntityZoneEntId(self.entId)

    def getZoneEntity(self):
        """returns zone entity for zone that contains this entity"""
        return self.level.getEntity(self.getZoneEntId())

    def getZoneNode(self):
        """returns zoneNode for zone that contains this entity"""
        return self.getZoneEntity().getNodePath()

    def privGetSetter(self, attrib):
        setFuncName = 'set%s%s' % (attrib[0].upper(), attrib[1:])
        if hasattr(self, setFuncName):
            return getattr(self, setFuncName)
        return None

    def callSetters(self, *attribs):
        """call this with a list of attribs, and any that exist on the
        entity and have setters will be passed to their setter"""
        self.privCallSetters(0, *attribs)

    def callSettersAndDelete(self, *attribs):
        """same as callSetters, but also removes attribs from entity"""
        self.privCallSetters(1, *attribs)

    def privCallSetters(self, doDelete, *attribs):
        """common implementation of callSetters and callSettersAndDelete"""
        for attrib in attribs:
            if hasattr(self, attrib):
                setter = self.privGetSetter(attrib)
                if setter is not None:
                    value = getattr(self, attrib)
                    if doDelete:
                        delattr(self, attrib)
                    setter(value)

    # this will be called with each item of our spec data on initialization
    def setAttribInit(self, attrib, value):
##         if __debug__:
##             if hasattr(self, attrib):
##                 Entity.notify.warning(
##                     '%s already has member %s in setAttribInit' %
##                     (self, attrib))
        # TODO: we should probably put this crep in a dictionary
        # rather than dump it into the entity's namespace
        self.__dict__[attrib] = value

    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('entId', '?'))+' '+message)

    if __dev__:
        # support for level editing
        def handleAttribChange(self, attrib, value):
            # call callback function if it exists
            # otherwise set attrib directly and call notify func
            setter = self.privGetSetter(attrib)
            if setter is not None:
                # call the setter
                setter(value)
            else:
                # set the attrib directly
                self.__dict__[attrib] = value
                # and call the notify func
                self.attribChanged(attrib, value)

        def attribChanged(self, attrib, value):
            """
            This is called when a parameter is tweaked and no setter
            is called; i.e. the value is set directly on the object.
            Some Entities might want to completely reset every time anything
            is tweaked; this is the place to do it, just override this func
            in your derived class
            """
            pass
