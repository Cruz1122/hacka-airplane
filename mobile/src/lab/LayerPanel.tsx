// Left panel: layer tree, front-most layer first (like design tools), with per-layer and
// per-object actions.
import { useState } from 'react';

import {
  deleteObject,
  duplicateObject,
  shiftLayer,
  shiftObject,
  updateLayer,
} from '@/onboarding/scene/doc';
import type { LayerId, SceneDoc } from '@/onboarding/scene/types';

import { Icon, type IconName } from './icons';

interface LayerPanelProps {
  doc: SceneDoc;
  apply: (doc: SceneDoc, key?: string) => void;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  onError: (message: string) => void;
}

function IconButton({
  icon,
  label,
  onClick,
  active,
}: {
  icon: IconName;
  label: string;
  onClick: () => void;
  active?: boolean;
}) {
  return (
    <button
      type="button"
      className={`lab-icon-btn${active ? ' is-active' : ''}`}
      title={label}
      aria-label={label}
      onClick={onClick}
    >
      <Icon name={icon} />
    </button>
  );
}

export function LayerPanel({ doc, apply, selectedId, onSelect, onError }: LayerPanelProps) {
  const [collapsed, setCollapsed] = useState<Set<LayerId>>(
    () => new Set(['sky', 'sun', 'uiOverlay', 'snowCap', 'crater']),
  );
  const toggle = (id: LayerId) =>
    setCollapsed((s) => {
      const next = new Set(s);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  const run = (fn: () => void) => {
    try {
      fn();
    } catch (e) {
      onError(e instanceof Error ? e.message : String(e));
    }
  };

  const layers = [...doc.layers].reverse();
  return (
    <div className="lab-layers">
      {layers.map((layer) => {
        const index = doc.layers.indexOf(layer) + 1;
        const open = !collapsed.has(layer.id) || layer.objects.some((o) => o.id === selectedId);
        return (
          <div key={layer.id} className={`lab-layer${layer.visible ? '' : ' is-hidden'}`}>
            <div className="lab-layer-row">
              <button
                type="button"
                className="lab-icon-btn"
                aria-label={open ? 'Contraer' : 'Expandir'}
                onClick={() => toggle(layer.id)}
              >
                <Icon name={open ? 'chevronDown' : 'chevronRight'} />
              </button>
              <IconButton
                icon={layer.visible ? 'eye' : 'eyeOff'}
                label={layer.visible ? 'Ocultar capa' : 'Mostrar capa'}
                onClick={() => apply(updateLayer(doc, layer.id, { visible: !layer.visible }))}
              />
              <IconButton
                icon={layer.locked ? 'lock' : 'unlock'}
                label={layer.locked ? 'Desbloquear capa' : 'Bloquear capa'}
                active={layer.locked}
                onClick={() => apply(updateLayer(doc, layer.id, { locked: !layer.locked }))}
              />
              <span className="lab-layer-name" title={`Profundidad ${layer.parallax}`}>
                <span className="lab-layer-index">{String(index).padStart(2, '0')}</span>{' '}
                {layer.name}
              </span>
              <IconButton
                icon="up"
                label="Subir capa (más adelante)"
                onClick={() => apply(shiftLayer(doc, layer.id, 1))}
              />
              <IconButton
                icon="down"
                label="Bajar capa (más atrás)"
                onClick={() => apply(shiftLayer(doc, layer.id, -1))}
              />
            </div>
            {open &&
              [...layer.objects].reverse().map((o) => (
                <div
                  key={o.id}
                  className={`lab-object-row${o.id === selectedId ? ' is-selected' : ''}`}
                >
                  <button
                    type="button"
                    className="lab-object-name"
                    onClick={() => onSelect(o.id)}
                    disabled={layer.locked}
                    title={layer.locked ? 'Capa bloqueada' : o.id}
                  >
                    {o.name}
                  </button>
                  {layer.id !== 'uiOverlay' && (
                    <>
                      <IconButton
                        icon="up"
                        label="Traer adelante"
                        onClick={() => apply(shiftObject(doc, o.id, 1))}
                      />
                      <IconButton
                        icon="down"
                        label="Enviar atrás"
                        onClick={() => apply(shiftObject(doc, o.id, -1))}
                      />
                      <IconButton
                        icon="copy"
                        label="Duplicar"
                        onClick={() =>
                          run(() => {
                            const r = duplicateObject(doc, o.id);
                            apply(r.doc);
                            onSelect(r.id);
                          })
                        }
                      />
                      <IconButton
                        icon="trash"
                        label="Eliminar"
                        onClick={() =>
                          run(() => {
                            apply(deleteObject(doc, o.id));
                            if (selectedId === o.id) onSelect(null);
                          })
                        }
                      />
                    </>
                  )}
                </div>
              ))}
          </div>
        );
      })}
    </div>
  );
}
