/*
 * Copyright (c) 2017 Valve Corporation
 * Copyright (c) 2017 LunarG, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Author: Lenny Komow <lenny@lunarg.com>
 */

#pragma once

#include <QEvent>
#include <QMainWindow>
#include <QSettings>
#include <QSplitter>

#include "active_layers_widget.h"
#include "layer_locations_widget.h"
#include "layer_settings_widget.h"
#include "override_settings.h"

class LayerManager : public QMainWindow
{
    Q_OBJECT
    
public:
    LayerManager();
    
protected:
    void closeEvent(QCloseEvent *event) override;
    
private slots:
    void resetAll();
    void saveAll();
    
private:
    QSettings settings;
    OverrideSettings override_settings;
    
    QSplitter *outer_split;
    QSplitter *inner_split;
    LayerLocationsWidget *locations;
    ActiveLayersWidget *active_layers;
    LayerSettingsWidget *layer_settings;
};
