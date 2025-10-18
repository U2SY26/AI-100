
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ChatInterface from './ChatInterface';

describe('ChatInterface', () => {
  it('renders the initial greeting message', () => {
    render(<ChatInterface />);
    expect(screen.getByText('안녕하세요! 무엇을 도와드릴까요?')).toBeInTheDocument();
  });
});
