// The two role cards, stacked, sharing the height they are given, each with its own Pet and
// pencil. One Pet's options open at a time, right under its card. The host owns the looks (the saved ones on the group screen, local ones
// in the design lab).
import { Fragment, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { fill, t } from '@/i18n';
import { wornBy, type PetLook, type PetLooks, type PetRole } from '@/state/petLook';

import { PetCustomizer } from '../PetCustomizer';
import { PET_NAME } from '../pet/petCore';
import { spacing } from '../theme/tokens';

import { RoleCard } from './RoleCard';

const ROLES: readonly PetRole[] = ['guide', 'visitor'];
const LABEL: Record<PetRole, string> = { guide: t.group.imGuide, visitor: t.group.imVisitor };
const HINT: Record<PetRole, string> = {
  guide: t.group.imGuideHint,
  visitor: t.group.imVisitorHint,
};

export interface RoleChoicesProps {
  looks: PetLooks;
  onLookChange: (role: PetRole, patch: Partial<PetLook>) => void;
  onChoose: (role: PetRole) => void;
  width: number;
  disabled?: boolean;
  /** Role currently animating into its session; highlights this card and softens the other. */
  selected?: PetRole | null;
  /** Controlled open customizer (e.g. so Android back can close it); uncontrolled when omitted. */
  editing?: PetRole | null;
  onEditingChange?: (role: PetRole | null) => void;
}

export function RoleChoices({
  looks,
  onLookChange,
  onChoose,
  width,
  disabled,
  selected = null,
  editing: controlledEditing,
  onEditingChange,
}: RoleChoicesProps) {
  const [localEditing, setLocalEditing] = useState<PetRole | null>(null);
  const editing = controlledEditing !== undefined ? controlledEditing : localEditing;
  const setEditing = (next: PetRole | null) => {
    if (controlledEditing === undefined) setLocalEditing(next);
    onEditingChange?.(next);
  };
  const g = t.group;
  return (
    <View style={styles.roles}>
      {ROLES.map((role, index) => (
        <Fragment key={role}>
          <RoleCard
            label={LABEL[role]}
            hint={HINT[role]}
            wears={wornBy(looks[role], role)}
            onPress={() => onChoose(role)}
            width={width}
            onEdit={() => setEditing(editing === role ? null : role)}
            editLabel={fill(g.pet.edit[role], { pet: PET_NAME })}
            editing={editing === role}
            selected={selected === role}
            dimmed={selected !== null && selected !== role}
            pulseDelay={index * 1400}
            disabled={disabled}
          />
          {editing === role && (
            <PetCustomizer
              role={role}
              look={looks[role]}
              onChange={(patch) => onLookChange(role, patch)}
              onDone={() => setEditing(null)}
            />
          )}
        </Fragment>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  roles: { flexGrow: 1, gap: spacing.md },
});
