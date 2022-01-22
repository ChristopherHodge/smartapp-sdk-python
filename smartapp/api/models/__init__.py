from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from smartapp.api.models import smartthings, smartapp

LifecycleBase     = smartapp.LifecycleBase
Install           = smartapp.Install
Configuration     = smartapp.Configuration
Confirmation      = smartapp.Confirmation
Update            = smartapp.Update
Event             = smartapp.Event
EventType         = smartapp.EventType
LifecycleResponse = smartapp.LifecycleResponse
SubscriptionType  = smartapp.SubscriptionType

class AuthToken(BaseModel):
    access_token:      Optional[str]
    refresh_token:     Optional[str]
    token_type:        Optional[str]
    error:             Optional[str]
    error_description: Optional[str]

class TokenRefresh(BaseModel):
    grant_type:    str
    refresh_token: str

class Version(BaseModel):
    version: str

class DeviceCollection(BaseModel):
    items: List[smartthings.Device] = []

class InstalledAppCollection(BaseModel):
    items: List[smartthings.InstalledApp] = []

class SubscriptionCollection(BaseModel):
    items: List[smartthings.Subscription] = []

class SceneCollection(BaseModel):
    items: List[smartthings.SceneSummary] = []

class AllLifecycles(smartapp.LifecycleBase):
    configurationData:  Optional[smartapp.ConfigurationData]
    confirmationData:   Optional[smartapp.ConfirmationData]
    eventData:          Optional[smartapp.EventData]
    installData:        Optional[smartapp.InstallData]
    updateData:         Optional[smartapp.UpdateData]
    oAuthCallbackData:  Optional[smartapp.OAuthCallbackData]
    uninstallData:      Optional[smartapp.UninstallData]
    pingData:           Optional[smartapp.PingData]

