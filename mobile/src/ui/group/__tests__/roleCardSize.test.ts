import { ROLE_CIRCLE_MAX, ROLE_CIRCLE_MIN, roleCircleSize } from '../roleCardSize';

const RESERVED = 71;

describe('roleCircleSize', () => {
  it('takes about half of a tall card', () => {
    expect(roleCircleSize(280, 358, RESERVED)).toBe(154);
  });

  it('grows with the card up to its ceiling', () => {
    expect(roleCircleSize(240, 358, RESERVED)).toBeLessThan(roleCircleSize(300, 358, RESERVED));
    expect(roleCircleSize(900, 600, RESERVED)).toBe(ROLE_CIRCLE_MAX);
  });

  it('leaves room for the label and padding on a short card', () => {
    const h = 168;
    expect(roleCircleSize(h, 358, RESERVED)).toBeLessThanOrEqual(h - RESERVED);
  });

  it('never shrinks below the floor or past the width share', () => {
    expect(roleCircleSize(60, 358, RESERVED)).toBe(ROLE_CIRCLE_MIN);
    expect(roleCircleSize(400, 200, RESERVED)).toBe(120);
  });
});
